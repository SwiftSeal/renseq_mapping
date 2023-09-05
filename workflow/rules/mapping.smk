rule get_contigs:
    input:
        contigs = get_reference(),
        result = "results/{experiment}/result.tsv"
    output:
        filtered_contigs = "results/{experiment}/reference/filtered_reference.fasta"
    run:
        with open(input.contigs) as fasta, open(input.result) as result, open(output.filtered_contigs, "w") as filtered:
            # get contigs to keep
            contigs = set()
            for line in result:
                fields = line.split("\t")
                contigs.add(fields[0])
            
            # write out contigs
            for record in SeqIO.parse(fasta, "fasta"):
                if record.id in contigs:
                    SeqIO.write(record, filtered, "fasta")

rule blast:
    input:
        contigs = "results/{experiment}/reference/filtered_reference.fasta",
        reference = config["mapping_reference"]
    output:
        "results/{experiment}/blast.txt"
    conda:
        "../envs/bowtie2.yaml"
    resources:
        mem_mb = 4000,
        partition = "short"
    shell:
        """
        blastn -query {input.contigs} -subject {input.reference} -outfmt 6 -out {output}
        """