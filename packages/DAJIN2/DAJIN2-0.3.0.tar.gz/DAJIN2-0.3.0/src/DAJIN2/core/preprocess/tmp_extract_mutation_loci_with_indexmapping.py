from __future__ import annotations

import re
from collections import defaultdict
import json
import numpy as np
from pathlib import Path
from typing import Generator
from scipy import stats
from scipy.spatial import distance
import pickle

# from sklearn.neighbors import LocalOutlierFactor
from DAJIN2.core.preprocess.extract_errors_in_homopolymer import extract_errors_in_homopolymer


def read_midsv(filepath) -> Generator[dict[str, str]]:
    with open(filepath, "r") as f:
        for line in f:
            yield json.loads(line)


def call_coverage_on_each_base(midsv_sample: Generator[dict], sequence: str, index_mapping: dict) -> list[int]:
    coverages = [1] * len(sequence)
    for samp in midsv_sample:
        for i, cs in enumerate(samp["CSSPLIT"].split(",")):
            if i not in index_mapping:
                continue
            if cs == "N":
                continue
            coverages[index_mapping[i]] += 1
    return coverages


def count_indels(midsv_sample, sequence: str, index_mapping: dict) -> dict[str, list[int]]:
    len_sequence = len(sequence)
    count = {"+": [0] * len_sequence, "-": [0] * len_sequence, "*": [0] * len_sequence}
    for samp in midsv_sample:
        for i, cs in enumerate(samp["CSSPLIT"].split(",")):
            if i not in index_mapping:
                continue
            if cs.startswith("=") or cs == "N" or re.search(r"a|c|g|t|n", cs):
                continue
            if cs.startswith("+"):
                # count["+"][i] += len(cs.split("|"))
                count["+"][i] += 1
            elif cs.startswith("-"):
                count["-"][i] += 1
            elif cs.startswith("*"):
                count["*"][i] += 1
    return count


def normalize_indels(count: dict[str, list[int]], coverages: list[int]) -> dict[str, np.array]:
    count_normalized = dict()
    coverages = np.array(coverages)
    for mut in count:
        counts = np.array(count[mut])
        count_normalized[mut] = counts / coverages
    return count_normalized


def split_kmer(indels: dict[str, np.array], kmer: int = 11) -> dict[str, np.array]:
    results = defaultdict(list)
    center = kmer // 2
    for mut, value in indels.items():
        for i in range(len(value)):
            if center <= i <= len(value) - center:
                start = i - center
                if kmer % 2 == 0:
                    end = i + center
                else:
                    end = i + center + 1
                results[mut].append(value[start:end])
            else:
                results[mut].append(np.array([0] * kmer))
    return results


def merge_peaks(indels_sample_normalized, mutation, peaks, hight):
    """Values higher than 75% quantile of the control values and the surrouings are peaks, merge it as a peak"""
    values_sample = indels_sample_normalized[mutation]
    for i, value in enumerate(values_sample):
        if i not in peaks and value > hight:
            for j in range(i - 5, i + 6):
                if j in peaks:
                    peaks.add(i)
                    break
    return peaks


def extract_dissimilar_loci(indels_kmer_sample: dict, indels_kmer_control: dict) -> dict[str, set]:
    """
    Comparing Sample and Control, the 'similar mean' and
    'similar variance' are considered as sequence errors.
    """
    results = dict()
    for mut in indels_kmer_sample:
        values_sample = indels_kmer_sample[mut]
        values_control = indels_kmer_control[mut]
        """
        Calculate cosine similarity: 1 means exactly same, 0 means completely different.
        Zero vector does not return correct value, so add epsilon (1e-10).
        example: distance.cosine([0,0,0], [1,2,3]) retuns 0.
        """
        cossims = [1 - distance.cosine(x + 1e-10, y + 1e-10) for x, y in zip(values_sample, values_control)]
        # Perform T-test: nan means exactly same, p > 0.05 means similar in average.
        t_pvalues = [stats.ttest_ind(x, y, equal_var=False)[1] for x, y in zip(values_sample, values_control)]
        t_pvalues = [1 if np.isnan(t) else t for t in t_pvalues]
        # Perform F-test: p > 0.05 means similar in variance.
        f_pvalues = [stats.bartlett(x, y)[1] for x, y in zip(values_sample, values_control)]
        # if pvalue == nan or pval > 0.05, samples and controls are similar.
        dissimilar_loci = set()
        for i, (cossim, t_pval, f_pval) in enumerate(zip(cossims, t_pvalues, f_pvalues)):
            # deletion may be the similar cossim, but t_val < 0.05. Others should be dissimilar.
            if (cossim > 0.9 and t_pval < 0.05) or (cossim < 0.9 and (t_pval < 0.05 or f_pval < 0.05)):
                dissimilar_loci.add(i)
        results[mut] = dissimilar_loci
    return results


def discard_errors_in_homopolymer(dissimilar_loci, errors_in_homopolymer) -> dict[str, set]:
    mutation_loci = dict()
    for mut in ["+", "-", "*"]:
        error_loci = errors_in_homopolymer[mut]
        mutation_loci[mut] = dissimilar_loci[mut] - error_loci
    return mutation_loci


def transpose_mutation_loci(mutation_loci: set[int], sequence: str) -> list[set]:
    mutation_loci_transposed = [set() for _ in range(len(sequence))]
    for mut, idx_mutation in mutation_loci.items():
        for i, loci in enumerate(mutation_loci_transposed):
            if i in idx_mutation:
                loci.add(mut)
    return mutation_loci_transposed


###########################################################
# main
###########################################################


def process_mutation_loci(TEMPDIR: Path, FASTA_ALLELES: dict, CONTROL_NAME: str) -> None:
    with open(Path(TEMPDIR, "mutation_loci", "index_mapping..pickle"), "rb") as f:
        INDEX_MAPPING = pickle.load(f)
    for allele, sequence in FASTA_ALLELES.items():
        index_mapping = INDEX_MAPPING.get(allele, {i: i for i in range(len(sequence))})
        index_mapping = {v: k for k, v in index_mapping.items()}
        filepath_control = Path(TEMPDIR, "midsv", f"{CONTROL_NAME}_{allele}.json")
        indels_control = count_indels(read_midsv(filepath_control), sequence, index_mapping)
        coverages_control = call_coverage_on_each_base(read_midsv(filepath_control), sequence, index_mapping)
        indels_control_normalized = normalize_indels(indels_control, coverages_control)
        indels_kmer_control = split_kmer(indels_control_normalized, kmer=11)
        # Save indels_control_normalized and indels_kmer_control as pickle to reuse in consensus calling
        with open(Path(TEMPDIR, "mutation_loci", f"{CONTROL_NAME}_{allele}_normalized..pickle"), "wb") as f:
            pickle.dump(indels_control_normalized, f)
        with open(Path(TEMPDIR, "mutation_loci", f"{CONTROL_NAME}_{allele}_kmer..pickle"), "wb") as f:
            pickle.dump(indels_kmer_control, f)


def update_mutation_loci(MUTATION_LOCI_ALLELES, INDEX_MAPPING) -> dict[str, list]:
    """
    Filter mutations that exists both in control and other alleles
    """
    mutation_loci_control = MUTATION_LOCI_ALLELES["control"]
    for allele in MUTATION_LOCI_ALLELES:
        if allele == "control":
            continue
        index_mapping = INDEX_MAPPING[allele]
        for i, mut_control in enumerate(mutation_loci_control):
            corresponded_mutation = mut_control & MUTATION_LOCI_ALLELES[allele][index_mapping[i]]
            if corresponded_mutation:
                MUTATION_LOCI_ALLELES[allele][i] = corresponded_mutation
            else:
                MUTATION_LOCI_ALLELES["control"][i] = set()
                MUTATION_LOCI_ALLELES[allele][index_mapping[i]] = set()
    return MUTATION_LOCI_ALLELES


def extract_mutation_loci(TEMPDIR: Path, FASTA_ALLELES: dict, SAMPLE_NAME: str, CONTROL_NAME: str) -> dict[str, list]:
    with open(Path(TEMPDIR, "mutation_loci", "index_mapping..pickle"), "rb") as f:
        INDEX_MAPPING = pickle.load(f)
    MUTATION_LOCI_ALLELES = dict()
    for allele, sequence in FASTA_ALLELES.items():
        filepath_sample = Path(TEMPDIR, "midsv", f"{SAMPLE_NAME}_{allele}.json")
        index_mapping = INDEX_MAPPING.get(allele, {i: i for i in range(len(sequence))})
        index_mapping = {v: k for k, v in index_mapping.items()}
        indels_sample = count_indels(read_midsv(filepath_sample), sequence, index_mapping)
        coverages_sample = call_coverage_on_each_base(read_midsv(filepath_sample), sequence, index_mapping)
        indels_sample_normalized = normalize_indels(indels_sample, coverages_sample)
        indels_kmer_sample = split_kmer(indels_sample_normalized, kmer=11)
        # Load indels_control_normalized and indels_kmer_control
        with open(Path(TEMPDIR, "mutation_loci", f"{CONTROL_NAME}_{allele}_normalized..pickle"), "rb") as f:
            indels_control_normalized = pickle.load(f)
        with open(Path(TEMPDIR, "mutation_loci", f"{CONTROL_NAME}_{allele}_kmer..pickle"), "rb") as f:
            indels_kmer_control = pickle.load(f)
        # Calculate dissimilar loci
        dissimilar_loci = extract_dissimilar_loci(indels_kmer_sample, indels_kmer_control)
        # Extract error loci in homopolymer regions
        errors_in_homopolymer = dict()
        for mut in ["+", "-", "*"]:
            indels_sample_mut = indels_sample_normalized[mut]
            indels_control_mut = indels_control_normalized[mut]
            candidate_loci = dissimilar_loci[mut]
            # candidate_loci = anomaly_loci[mut] & dissimilar_loci[mut]
            errors_in_homopolymer[mut] = extract_errors_in_homopolymer(
                indels_sample_mut, indels_control_mut, sequence, candidate_loci
            )
        mutation_loci = discard_errors_in_homopolymer(dissimilar_loci, errors_in_homopolymer)
        mutation_loci_transposed = transpose_mutation_loci(mutation_loci, sequence)
        MUTATION_LOCI_ALLELES[allele] = mutation_loci_transposed
    MUTATION_LOCI_ALLELES = update_mutation_loci(MUTATION_LOCI_ALLELES, INDEX_MAPPING)
    return MUTATION_LOCI_ALLELES
