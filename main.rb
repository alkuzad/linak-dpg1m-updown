require 'libdeflate'

decompressor = Libdeflate::Decompressor.new

pathToDecompress = ARGV[0]

fileToDecompress = File.open(pathToDecompress, 'rb')

data = decompressor.decompress(fileToDecompress.read)

outputPath = "#{pathToDecompress}.decompressed"

File.open(outputPath, "wb") do |fil|
    puts "Writing decompressed data to #{outputPath}"
    fil.write(data)
end
