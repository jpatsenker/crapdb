import string

header = None

#convert into csv and get header
with open("superfamily/genomes", "r") as reader:
	line1 = reader.readline()
	line2 = reader.readline()
	line3 = reader.readline()

	header = map(string.lstrip, map(string.rstrip, line2.split('|')))[1:-1]
	assert header == ['genome', 'name', 'include', 'excuse', 'domain', 'comment', 'taxonomy', 'taxon_id', 'download_link', 'download_date', 'gene_link', 'homepage', 'password', 'parse', 'order1', 'supfam', 'order2']

	with open("superfamily/genomeInfo.csv", "w") as writer:
		map(
			lambda line: writer.write(
				str(
					reduce(
						lambda x, y:
							x+','+y,
						map(
							string.lstrip,
							map(string.rstrip, line.split('|')))[1:-1],
						"")
				+ "\n")[1:]),
			reader)

with open("superfamily/genomeInfo.csv", "r") as csvReader:
	with open("superfamily/filteredGenomeInfo.csv", "w") as csvWriter:
		map(
			lambda line:
				csvWriter.write(line.split(",")[1] + "," + line.split(",")[8] + "\n"),
			csvReader)
