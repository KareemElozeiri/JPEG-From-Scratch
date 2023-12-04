import numpy as np
class AritCoding:
    def __init__(self,data):
        self.symbols=list(set(data))
        self.precision=32
        self.whole=2**self.precision
        self.half=self.whole/2
        self.quarter=self.whole/4
        self.counts=self.calcFreqs(data)
        self.R=sum(self.counts)
        self.cumm=self.calcCum(data)
        
    def calcFreqs(self, data):
        freqs=[]
        for sym in self.symbols:
            freq=data.count(sym)
            freqs.append(freq)
                
        return freqs
        
    def calcCum(self,data):
        c= []
        n = len(data)
        c.append(0)
        for i in range(n):
            c.append(sum(self.counts[0:i+1]))
        c = np.array(c)
        return c
    
    def encode(self,sequence):
        src_code=[]
        s=0
        a= 0
        b=self.whole
        k=len(sequence)  
        for i in range(k):
            this_symbol_index = self.symbols.index(sequence[i])
            h = b-a
            b = a + (h*self.cumm[this_symbol_index+1]//self.R)
            a = a + (h*self.cumm[this_symbol_index]//self.R)
            
            dummy=0
            while ((b<self.half) or (a>=self.half)):
                if(b<self.half):

                    src_code.append('0')
                    if s!=0:
                        src_code.append('1'*s)
                    s=0
                    a=2*a
                    b=2*b
                elif(a>=self.half):
                    src_code.append('1')
                    if s!=0:
                        src_code.append('0'*s)
                    s=0
                    a= (2* (a-self.half))
                    b= (2* (b-self.half))
            while ((a>self.quarter) and (b<3*self.quarter)):
                s+=1
                a= 2*(a-self.quarter)
                b= 2*(b-self.quarter)

        s+=1
        if a<=self.quarter: 
            src_code.append('0')
            if s!=0:
                src_code.append('1'*s)
        else:
            src_code.append('1')
            if s!=0:
                src_code.append('0'*s)
        
        src_code=''.join(src_code)
        
        return src_code
  
  
    def decode(self,stream,eof):
        decoded_sequence=[]
        a=0
        b=self.whole
        n = len(self.symbols)
        M=len(stream)
        
        decimal_value=0
        j=1
        while j<=self.precision and j<=M:
            if stream[j-1]=='1':
                decimal_value+= 2**(self.precision-j)
            j+=1
        
        
        flag=0
        while not flag:
            for i in range(n):
                w= b-a
                b_= a + (w*self.cumm[i+1]) //self.R
                a_= a + (w*self.cumm[i]) //self.R
                if a_<=decimal_value and decimal_value<b_:
                    decoded_sequence.append(self.symbols[i])
                    a=a_
                    b=b_
                    if(self.symbols[i]==eof):
                        flag=1
                    break

            while 1:
                if b<self.half:
                    a*=2
                    b*=2
                    decimal_value*=2
                    if j<=M:
                        decimal_value+=int(stream[j-1])
                        j+=1
                elif a>=self.half:
                    a=2*(a-self.half)
                    b=2*(b-self.half)
                    decimal_value=2*(decimal_value-self.half)
                    if j<=M:
                        decimal_value+=int(stream[j-1])
                        j+=1
                
                elif a>=self.quarter and b<3*self.quarter:
                    a= 2*(a-self.quarter)
                    b= 2*(b-self.quarter)
                    decimal_value=2*(decimal_value-self.quarter)
                    if j<= M:
                        decimal_value+=int(stream[j-1])
                        j+=1
                else:
                    break
        
        decoded_sequence.pop()
            
        return decoded_sequence
        
        
        
# test
# seq= list(range(256))
# seq=seq*100
# eof='/'
# seq.append(eof)
# AC= AritCoding(seq)
# code= AC.encode(seq)
# print(code)
# decoded=AC.decode(code,eof)
# print(decoded)
# seq.pop()
# print('Same?? ',decoded==seq)
