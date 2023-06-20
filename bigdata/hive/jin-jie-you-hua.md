# 进阶优化

## 1. 存储格式和压缩算法

在Hive命令行中，用于指定不同的表存储格式的关键词如下

* 文本格式：TEXTFILE
* 序列化文件格式：SEQUENCEFILE
* RC文件格式：RCFILE
* ORC文件格式：ORC
* AVRO文件格式：AVRO
* Parquet文件格式：PARQUET

这些存储格式在Hive中主要有以下区别：

1. 存储方式：不同的存储格式采用不同的存储方式，如文本格式以纯文本形式存储，序列化文件格式以二进制序列化形式存储，ORC文件格式以行列混合存储形式存储等。
2. 存储效率：不同的存储格式对存储效率有不同的影响，如序列化文件格式和ORC文件格式采用列式存储，可以大幅减少IO操作的次数，提高存储效率；而文本格式则不支持列式存储，效率相对较低。
3. 压缩支持：不同的存储格式对压缩有不同的支持，如ORC文件格式和RC文件格式支持多种压缩算法，可以在减少存储空间的同时提高IO效率；而文本格式则不支持压缩。
4. 兼容性：不同的存储格式对兼容性有不同的要求，如Avro文件格式支持多种语言的序列化和反序列化，并支持架构演化，适用于多语言环境下的数据交换；而其他存储格式则可能不支持跨语言的数据交换。
5. 处理方式：不同的存储格式在查询和处理时可能有不同的方式，如列式存储的数据在执行聚合查询时效率更高，因为只需要扫描需要的列；而行式存储的数据则在执行全表扫描时效率更高，因为只需要扫描一行的数据。

例如对于电商用户行为分析，建议使用列式存储的存储格式，如ORC文件格式或Parquet文件格式。这是因为电商用户行为数据通常包含大量的字段，而列式存储可以只读取所需的列，减少IO操作的次数，提高查询效率；此外，列式存储通常支持更好的压缩比率，可以减少存储空间的占用。与行式存储相比，列式存储在数据分析和处理方面具有更好的性能和扩展性，因此在大数据场景下，列式存储格式是更加有效率的选择。同时，ORC文件格式和Parquet文件格式都支持多种压缩算法，可以在减少存储空间的同时提高IO效率，这对于电商用户行为数据的存储和分析非常有帮助。

ORC文件格式和Parquet文件格式都支持多种压缩算法，并且Hive默认会对这些文件格式进行自动压缩和解压。Hive提供了一些配置参数，可以指定默认的压缩算法和压缩级别，以及是否对所有文件进行压缩。

在命令行使用`SET hive.exec.compress.output=true`启用语法输出压缩，仅在当前会话有效，创建表时可以使用`STORED AS ORC TBLPROPERTIES("orc.compress"="SNAPPY")`的语法指定ORC文件格式使用SNAPPY压缩算法；

除了SNAPPY压缩算法，ORC文件格式和Parquet文件格式还支持多种其他的压缩算法，包括但不限于：

| 算法        | 压缩率 | 解压缩速度 |
| --------- | --- | ----- |
| GZIP、ZLIB | 较高  | 较慢    |
| BZIP2     | 较高  | 很慢    |
| LZO       | 较低  |  快    |
| LZ4       | 较低  | 很快    |
| SNAPPY    | 较低  | 很快    |

除了`hive.exec.compress.output`和`TBLPROPERTIES`语法外，Hive还提供了一些其他的配置参数，具体如下

<table><thead><tr><th width="211.5"></th><th></th></tr></thead><tbody><tr><td>mapreduce.map.output.compress</td><td>这个参数指定Map任务输出时是否进行压缩，默认值为false。如果将其设置为true，Map任务输出的中间结果会被压缩，从而减少磁盘IO和网络传输的开销。用户可以通过设置<code>mapreduce.map.output.compress.codec</code>来指定压缩算法，默认值为org.apache.hadoop.io.compress.SnappyCodec。</td></tr><tr><td>mapreduce.output.fileoutputformat.compress</td><td>这个参数指定Reduce任务输出时是否进行压缩，默认值为false。如果将其设置为true，Reduce任务输出的结果会被压缩，从而减少磁盘IO和网络传输的开销。用户可以通过设置<code>mapreduce.output.fileoutputformat.compress.codec</code>来指定压缩算法，默认值为org.apache.hadoop.io.compress.SnappyCodec。</td></tr><tr><td>mapreduce.output.fileoutputformat.compress.type</td><td>这个参数指定输出文件的数据的压缩格式，默认值为RECORD，表示压缩单个记录。如果将其设置为BLOCK，则表示压缩块，可以提高压缩率，但会影响查询性能。如果数据量较小，可以使用RECORD格式的压缩，以获得较好的压缩率和较高的解压缩速度。如果数据量较大，可以考虑使用BLOCK格式的压缩，以获得更高的压缩率。</td></tr><tr><td>mapreduce.output.fileoutputformat.compress.level</td><td>这个参数指定压缩级别，默认值为1，表示快速压缩。可以设置为0~9之间的整数，表示不同的压缩级别，级别越高，压缩率越高，但压缩速度越慢。</td></tr><tr><td>mapreduce.output.fileoutputformat.compress.codec</td><td>这个参数指定压缩算法，默认值为org.apache.hadoop.io.compress.SnappyCodec。用户可以通过设置该参数来指定其他的压缩算法，如org.apache.hadoop.io.compress.GzipCodec、org.apache.hadoop.io.compress.BZip2Codec等。</td></tr></tbody></table>

{% hint style="info" %}
Q：我是否可以这样理解，record是对每一条数据都用了压缩算法，而block是对整个数据用了压缩算法？

A：您的理解基本正确。在Hadoop中，压缩算法通常是基于数据块进行压缩的。当`mapreduce.output.fileoutputformat.compress.type`参数设置为RECORD时，每个数据记录都会被单独压缩，这可以获得较好的压缩比，同时也使得解压缩操作更加高效，因为每个记录都可以单独解压缩。而当该参数设置为BLOCK时，多个数据记录被组合成一个块，然后对整个块进行压缩，这样可以获得更高的压缩比，但解压缩操作需要对整个块进行解压缩，因此可能会更加耗时。

需要注意的是，RECORD和BLOCK并不是对每条数据或整个数据都使用了压缩算法，而是指定了压缩的粒度。实际上，每个数据块中的数据都会被压缩，无论是使用RECORD还是BLOCK方式。RECORD方式将每个数据记录单独压缩，而BLOCK方式将多个数据记录组合成一个块，然后对整个块进行压缩。因此，RECORD方式可以获得更好的压缩比，但解压缩操作可能更加高效；而BLOCK方式可以获得更高的压缩比，但解压缩操作可能更加耗时。
{% endhint %}

