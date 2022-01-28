#!/usr/bin/env python

import getpass
import os

# Required user input:
# 1) Which fusion prediction tools should be executed (tools)
# 2) Which post-processing steps should be executed (fd_tools)
# 3) Which reference data shall be used (ref_trans_version & ref_genome_build)
# 4) To whom shall slurm mails be sent to (receiver)

version = "1.3.4"

pipeline_name = "EasyFuse"

#tools=Readfilter,Mapsplice,Fusioncatcher,Star,Starfusion,Infusion,Fetchdata,Summary
tools = ("QC",
         "Readfilter",
         "Fusioncatcher",
         "Star",
         "Starfusion",
         "Infusion",
         "Mapsplice",
         "Soapfuse",
         "Fetchdata",
         "Summary")

fusiontools = ("Fusioncatcher",
               "Starfusion",
               "Infusion",
               "Mapsplice",
               "Soapfuse")

#fd_tools=Fusiongrep,Contextseq,Starindex,Staralign,Bamindex,Requantify
fd_tools = ("Fusiongrep",
            "Contextseq",
            "Starindex",
            "ReadFilter2",
            "ReadFilter2b",
            "StaralignBest",
            "BamindexBest",
            "RequantifyBest")

sender = "sender@mail.com"
receiver = "yegor@amazon.com"
min_read_len_perc = 0.75
max_dist_proper_pair = 200000
cis_near_distance = 1000000
model_pred_threshold = 0.75
tsl_filter = "4,5,NA"
requant_mode = ["best"]
context_seq_len = 400
ref_genome_build = "hg38"
ref_trans_version = "ensembl"
queueing_system = "slurm"
time_limit = "30-00:00:0"
partition = "queue1"
user = getpass.getuser()
module_dir = os.path.dirname(os.path.realpath(__file__))
#logfile=/data/urla_progs/TronData/ngs_pipelines/easyfuse/fusion.log
#fusion_db=/data/urla_progs/TronData/ngs_pipelines/easyfuse/fusion.db

# Define ressource usage (cpu (number of threads), mem (ram in Gb)):
resources = {
    "qc": {
        "cpu": 8,
        "mem": 10
    },
    "readfilter": {
        "cpu": 8,
        "mem": 50
    },
    "star": {
        "cpu": 16,
        "mem": 40
    },
    "kallisto": {
        "cpu": 16,
        "mem": 10
    },
    "mapsplice": {
        "cpu": 16,
        "mem": 30
    },
    "fusioncatcher": {
        "cpu": 16,
        "mem": 30
    },
    "starfusion": {
        "cpu": 32,
        "mem": 30
    },
    "starchip": {
        "cpu": 16,
        "mem": 30
    },
    "infusion": {
        "cpu": 32,
        "mem": 30
    },
    "soapfuse": {
        "cpu": 32,
        "mem": 20
    },
    "classification": {
        "cpu": 16,
        "mem": 16
    },
    "fetchdata": {
        "cpu": 16,
        "mem": 50
    },
    "summary": {
        "cpu": 8,
        "mem": 16
    }
}

# execution command for individual programs (what you write here should be identical to what is typed in the console)
commands = {
    # for qc
    "fastqc": "/home/sarus/bin/sarus run --mount=type=bind,source=/fsx,destination=/fsx tronbioinformatics/easyfuse:1.3.4 /code/FastQC/fastqc",
    "skewer": "/home/sarus/bin/sarus run --mount=type=bind,source=/fsx,destination=/fsx tronbioinformatics/easyfuse:1.3.4 /code/skewer-0.2.2/skewer",
    # for processing
    "mapsplice": "/home/sarus/bin/sarus run --mount=type=bind,source=/fsx,destination=/fsx tronbioinformatics/easyfuse:1.3.4 mapsplice.py",
    "fusioncatcher": "/home/sarus/bin/sarus run --mount=type=bind,source=/fsx,destination=/fsx tronbioinformatics/easyfuse:1.3.4 /code/fusioncatcher/1.0/bin/fusioncatcher",
    "starfusion": "/home/sarus/bin/sarus run --mount=type=bind,source=/fsx,destination=/fsx tronbioinformatics/easyfuse:1.3.4 STAR-Fusion",
    "infusion": "/home/sarus/bin/sarus run --mount=type=bind,source=/fsx,destination=/fsx --mount=type=bind,source=/fsx/ref,destination=/ref tronbioinformatics/easyfuse:1.3.4 /code/InFusion-0.8/infusion",
    "soapfuse": "/code/SOAPfuse/1.27/SOAPfuse-RUN.pl", #this is taken from the docker image so it doesn't matter
    # for processing and fetch data
    "star": "/home/sarus/bin/sarus run --mount=type=bind,source=/fsx,destination=/fsx tronbioinformatics/easyfuse:1.3.4 /code/STAR-2.6.1d/bin/Linux_x86_64/STAR",
    "samtools": "/home/sarus/bin/sarus run --mount=type=bind,source=/fsx,destination=/fsx tronbioinformatics/easyfuse:1.3.4 samtools",
    # for liftover
    "crossmap": "/home/sarus/bin/sarus run --mount=type=bind,source=/fsx,destination=/fsx tronbioinformatics/easyfuse:1.3.4 test",
    # supporting easyfuse scripts
    "qc_parser": "/home/sarus/bin/sarus run --mount=type=bind,source=/fsx,destination=/fsx tronbioinformatics/easyfuse:1.3.4 /code/easyfuse-1.3.4/misc/qc_parser.py",
    "skewer_wrapper": "/home/sarus/bin/sarus run --mount=type=bind,source=/fsx,destination=/fsx tronbioinformatics/easyfuse:1.3.4 /code/easyfuse-1.3.4/tool_wrapper/skewer_wrapper.py",
    "soapfuse_wrapper": "/home/sarus/bin/sarus run --mount=type=bind,source=/fsx/ref,destination=/ref --mount=type=bind,source=/fsx,destination=/fsx tronbioinformatics/easyfuse:1.3.4 /code/easyfuse-1.3.4/tool_wrapper/soapfuse_wrapper.py",
    "summarize": "/home/sarus/bin/sarus run --mount=type=bind,source=/fsx,destination=/fsx tronbioinformatics/easyfuse:1.3.4 /code/easyfuse-1.3.4/summarize_data.py",
    "fusionreadfilter": "/home/sarus/bin/sarus run --mount=type=bind,source=/fsx,destination=/fsx tronbioinformatics/easyfuse:1.3.4 /code/easyfuse-1.3.4/fusionreadfilter.py",
    "fetchdata": "/home/sarus/bin/sarus run --mount=type=bind,source=/fsx/ref,destination=/ref --mount=type=bind,source=/fsx,destination=/fsx tronbioinformatics/easyfuse:1.3.4 /code/easyfuse-1.3.4/fetchdata.py",
    "samples": "/home/sarus/bin/sarus run --mount=type=bind,source=/fsx,destination=/fsx tronbioinformatics/easyfuse:1.3.4 /code/easyfuse-1.3.4/misc/samples.py"
}
# full path to reference files
references = {
    "genome_fasta": "/fsx/ref/Homo_sapiens.GRCh38.dna.primary_assembly.fa",
    "genome_fastadir": "/fsx/ref/fasta",
    "genome_sizes": "/fsx/ref/STAR_idx/chrNameLength.txt",
    "genes_fasta": "/fsx/ref/Homo_sapiens.GRCh38.cdna.all.fa",
    "genes_gtf": "/fsx/ref/Homo_sapiens.GRCh38.86.gtf",
    "genes_adb": "/fsx/ref/Homo_sapiens.GRCh38.86.gff3.db",
    "genes_tsl": "/fsx/ref/Homo_sapiens.GRCh38.86.gtf.tsl"
}

# full path to program indices
indices = {
    "star": "/fsx/ref/star_index/",
    "bowtie": "/fsx/ref/bowtie_index/hg38",
    "starfusion": "/fsx/ref/starfusion_index/",
    "fusioncatcher": "/fsx/ref/fusioncatcher_index/"
}
# full path to program specific config files (these are just general files which need no user modification)
other_files = {
    "infusion_cfg": "/fsx/ref/infusion.cfg",
    "soapfuse_cfg": "/fsx/ref/soapfuse.cfg",
    "easyfuse_model": os.path.join(module_dir, "data", "model", "Fusion_modeling_FFPE_train_v32.random_forest.model_full_data.EF_full.rds")
}