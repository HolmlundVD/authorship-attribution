class arithmetic_coding(object):
    #
    #takes a frequency dictionary from a text and returns 
    #a dictionary containing the costs of each character
    #
    @staticmethod
    def arithmetic_coding_algorithm(frequency_dict:dict):
        costs=dict()       
        list_of_frequencies=sorted(frequency_dict.items(),key=lambda token:-token[1])
        
        arithmetic_coding.__split_dictionary(list_of_frequencies,costs,0)
        return costs
    def __init__(self,frequency_table:dict):
        self.costs=arithmetic_coding.arithmetic_coding_algorithm(frequency_table)
        self.max_val=0
        for element in self.costs.values():
            if element>self.max_val:
                self.max_val=element
    def cost_of_text(self,frequency_table:dict):
        cost=0
        for token in frequency_table.items():
            cost+=self.costs[token[0]]*token[1]
        return cost
    #
    #to be called recursively. given a list of tuples a empty dictionary and the current depth
    #will split said list into two parts and assign the tokens in the list costs based on their frequency
    #
    @staticmethod        
    def __split_dictionary(to_split:list,costs:dict,depth:int):
        if len(to_split)==0:
            return 
        total=sum([pair[1] for pair in to_split])
        
        count=0        
        first_half=[]
        second_half=[]
        half_reached=False
        for token in to_split:
            before=count            
            count+=token[1]
            after=count
            if half_reached:                
                second_half.append(token)
            else:
                if count>=total/2:
                    half_reached=True
                    if abs(total/2-after)>abs(total/2-before):
                        
                        second_half.append(token)
                    else:
                       
                        first_half.append(token)
                else:
                    first_half.append(token)
            
        if len(first_half)==1:
            
            costs[first_half[0]]=depth+1
            if len(second_half)==1:                
                costs[second_half[0]]=depth+1
            else:                              
                arithmetic_coding.__split_dictionary(second_half,costs,depth+1)
        else:                       
            arithmetic_coding.__split_dictionary(first_half,costs,depth+1)            
            arithmetic_coding.__split_dictionary(second_half,costs,depth+1)


