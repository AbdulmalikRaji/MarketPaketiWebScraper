#from Props import StaticProps as SP
#from Logger import LogManager as LM

class DataHelper(object):
    #TODO insert try catch
    @staticmethod
    def slicedata(data, slice_len):
        it = iter(data)
        while True:
            items = []
            for index in range(slice_len):
                try:
                    item = next(it)
                except StopIteration:
                    if items == []:
                        return # we are done
                    else:
                        break # exits the "for" loop
                items.append(item)
            yield items
