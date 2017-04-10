######不同的libsvm数据合并,new_add数据的index自动在base基础上递增
from six import iteritems, PY2, PY3, string_types, text_type
from util import BigFileSort
import logging
import time
from __future__ import print_function, unicode_literals
from collections import OrderedDict ## sort new feature index 

def safe_float(text, replace_dict=None):
    """
    Attempts to convert a string to an int, and then a float, but if neither is
    possible, just returns the original string value.
    :param text: The text to convert.
    :type text: str
    :param replace_dict: Mapping from text to replacement text values. This is
                         mainly used for collapsing multiple labels into a
                         single class. Replacing happens before conversion to
                         floats. Anything not in the mapping will be kept the
                         same.
    :type replace_dict: dict from str to str
    """

    # convert to text to be "Safe"!
    text = text_type(text)

    if replace_dict is not None:
        if text in replace_dict:
            text = replace_dict[text]
        else:
            logging.getLogger(__name__).warning('Encountered value that was '
                                                'not in replacement '
                                                'dictionary (e.g., class_map):'
                                                ' {}'.format(text))
    try:
        return int(text)
    except ValueError:
        try:
            return float(text)
        except ValueError:
            return text.decode('utf-8') if PY2 else text
        except TypeError:
            return 0.0
    except TypeError:
        return 0
#print safe_float('g23e')
def _pair_to_tuple(pair, base_indexRange,feat_map=None):
    """
    Split a feature-value pair separated by a colon into a tuple.  Also
    do safe_float conversion on the value.
    """
    name, value = pair.split(':')
    if feat_map is not None:
        name = feat_map[name]
    value = safe_float(value)
    name = safe_float(name)+base_indexRange#base数据max(feature_index)
    return (name, value)
#print _pair_to_tuple('g23e:1')


def mergeLine(base,new_add,fp_merge_outFile,indexEq):
    new_add_match=new_add[1:]
    if indexEq:
        curr_info_dict = dict(_pair_to_tuple(pair, 100,feat_map=None) for pair in new_add_match)
        curr_info_dict = OrderedDict(sorted(curr_info_dict.items(),key = lambda t:t[0]))
        print('{}'.format(new_add[0]), end=' ', file=fp_merge_outFile)
        print('{}'.format(' '.join(base[1:])), end=' ', file=fp_merge_outFile)
        print(' '.join(('{}:{}'.format(field, value) for field, value in curr_info_dict.iteritems())) ,end='\n', file=fp_merge_outFile)
    else:
        curr_info_dict = dict(_pair_to_tuple(pair, 100,feat_map=None) for pair in new_add_match)
        curr_info_dict = OrderedDict(sorted(curr_info_dict.items(),key = lambda t:t[0]))
        print('{}'.format(new_add[0]), end=' ', file=fp_merge_outFile)
        print(' '.join(('{}:{}'.format(field, value) for field, value in curr_info_dict.iteritems())) ,end='\n', file=fp_merge_outFile)
def mergeFile(file_base,file_new_add,file_merge,file_base_sorted,file_new_add_sorted):
    logger = logging.getLogger(__name__)
    logger.info('Checking job results')
    start=time.clock()
    ######sort key first using code:big_file_sort
    '''先对需要合并的数据排序'''
    BigFileSort.sort_file(file_base,file_base_sorted)
    BigFileSort.sort_file(file_new_add,file_new_add_sorted)
    if file_base_sorted:
        fp_base = open(file_base_sorted,"r")
    if file_new_add_sorted:
        fp_new_add = open(file_new_add_sorted,"r")
    fp_merge = open(file_merge,"w")

    base_line = fp_base.readline()
    new_add_line = fp_new_add.readline()
    
    while base_line and new_add_line:
        base = base_line.strip().split()
        new_add = new_add_line.strip().split()

        if base[0] < new_add[0]:
            fp_merge.write(base_line)
            base_line = fp_base.readline()
        elif base[0] > new_add[0]:
            '''新增文件的feature index需要在base的基础上递增base_indexRange'''
            mergeLine(base,new_add,fp_merge,indexEq=False)
            new_add_line = fp_new_add.readline()
        else:    
            '''新增文件合并两个文件的feature index'''
            mergeLine(base,new_add,fp_merge,indexEq=True)
            base_line = fp_base.readline()
            new_add_line = fp_new_add.readline()
            continue
        
    if base_line:
        fp_merge.write(base_line)
        for line in fp_base:
            fp_merge.write(line)
    if new_add_line:
        fp_merge.write(new_add_line)
        for line in fp_new_add:
            fp_merge.write(line)  
            
    fp_merge.close()
    fp_base.close()
    fp_new_add.close()
    end=time.clock()
    print("Running time: %s seconds"%(end-start))
mergeFile('./data/userid_search_vectors2.txt','./data/userid_app_doclevel_vectors.txt','merge_search-app_info.libsvm','./data/userid_search_vectors2.sorted','./data/userid_app_doclevel_vectors.sorted')