### MergeBigFile
用于合并不同来源的libsvm文件，其他类型的大文件合并可根据需要修改，自定义函数mergeLine即可。

#### 关键步骤

- 排序需要合并的文件
- 定义base文本最大feature index
- feature index不同时原样输出base文件的userID和features，new_add文件的userID和(featureIndex+base_indexRange):value
- feature index相同时合并二者feature并输出

#### example

```python
'''
 * baseFile
 * new_addFile
 * Merge_outFile
 * baseFile_sorted
 * new_addFile_sorted
'''
mergeFile('./data/userid_search_vectors2.txt','./data/userid_app_doclevel_vectors.txt','merge_search-app_info4.libsvm','./data/userid_search_vectors2.sorted','./data/userid_app_doclevel_vectors.sorted')
```

