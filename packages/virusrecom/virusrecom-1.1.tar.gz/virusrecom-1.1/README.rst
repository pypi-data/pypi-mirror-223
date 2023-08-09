### VirusRecom: Detecting recombination of viral lineages using information theory

### Getting help
virusrecom is a command line interface program, users can get help documentation of the software by entering  ```virusrecom -h ``` or  ```virusrecom --help ```. 

<b>For detailed documentation, please refer to https://github.com/ZhijianZhou01/virusrecom/

<b>The simple help documentation of virusrecom v1.1 is as follows.</b>

| Parameter | Description |
| --- | --- |
|-h, --help | Show this help message and exit.|
|-a ALIGNMENT | Aligned sequence file (*.fasta). Note, each sequence name requires containing lineage mark.|
|-ua UNALIGNMENT | Unaligned (non-alignment) sequence file (*.fasta). Note, each sequence name requires containing lineage mark.|
|-at ALIGN_TOOL | Program used for multiple sequence alignments (MSA).|
|-iwic INPUT_WIC | Using the already obtained WIC values of reference lineages directly by a *.csv input-file.|
|-q QUERY | Name of query lineage (usually potential recombinant), such as ‘-q xxxx’. Besides, ‘-q auto’ can scan all lineages as potential recombinant in turn.|
|-l LINEAGES | Path of a text-file containing multiple lineage marks.|
|-g GAP | Reserve sites containing gap in subsequent analyses? ‘-g y’means to reserve, and ‘-g n’ means to delete.|
|-m METHOD | Method for scanning. ‘-m p’ means use polymorphic sites only, ‘-m a’ means use all the sites.|
|-w WINDOW | Number of nucleotides sites per sliding window. Note: if the ‘-m p’ has been used, -w refers to the number of polymorphic sites per windows.|
|-s STEP | Step size of the sliding window. Note: if the ‘-m p’ has been used, -s refers to the number of polymorphic sites per jump.|
|-mr MAX_REGION | The maximum allowed recombination region. Note: if the ‘-m p’ method has been used, it refers the maximum number of polymorphic sites contained in a recombinant region.|
|-cp PERCENTAGE | The cutoff threshold of proportion (cp, default: 0.9) used for searching recombination regions when mWIC/EIC >= cp, the maximum value of cp is 1.|
|-cu CUMULATIVE | Simply using the max cumulative WIC of all sites to identify the major parent. Off by default. If required, specify ‘-cu y.|
|-b BREAKPOINT | Possible breakpoint scan of recombination. ‘-b y’ means yes, ‘-b n’ means no. Note: this option only takes effect when ‘-m p’ has been specified.|
| -bw BREAKWIN | The window size (default: 200) used for breakpoint scan. The step size is fixed at 1. Note: this option only takes effect when ‘-m p -b y’ has been specified.|
|-t THREAD | Number of threads (default: 1) used for MAS.|
|-y Y_START | Starting value (default: 0) of the Y-axis in plot diagram.|
|-le LEGEND | The location of the legend, the default is adaptive. '-le r' indicates placed on the right.|
|-owic ONLY_WIC | Only calculate site WIC value. Off by default. If required, please specify ‘-owic y’.|
|-e ENGRAVE | Engraves file name to sequence names in batches. By specifying a directory containing one or multiple sequence files (*.fasta).|
|-en EXPORT_NAME | Export all sequence name of a *.fasta file.|
|-o | Output directory to store all results.|

### Citation
Zhou ZJ, Yang CH, Ye SB, Yu XW, Qiu Y, Ge XY. VirusRecom: an information-theory-based method for recombination detection of viral lineages and its application on SARS-CoV-2. Brief Bioinform. 2023 Jan 19;24(1):bbac513. doi: 10.1093/bib/bbac513. PMID: 36567622.

