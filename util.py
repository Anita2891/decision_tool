class Util:

    def __init__(self):
        pass

    #convert string data in to array
    def convertStringArray(inputString,firstDelimiter='&', secondDelimeter='='):
        firstArray = inputString.split(firstDelimiter)
        res=dict()
        for item in firstArray:
            newSplit= item.split(secondDelimeter)
            key= newSplit[0]
            value= newSplit[1]
            res[key]=value
        return res

    def colorNegativeRed(self,val):
         color = 'red' if val< 0 else 'black'
         return f'color: {color}'
