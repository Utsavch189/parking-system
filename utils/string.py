import re
 
class StringBuilder:

    def __init__(self,string:str) -> None:
        self.string=string

    def normalize_spaces(self)->'StringBuilder':
        return StringBuilder(re.sub(r'\s+', ' ', self.string).strip())
    
    def uppercase(self)->'StringBuilder':
        return StringBuilder(self.string.upper())
    
    def lowercase(self)->'StringBuilder':
        return StringBuilder(self.string.lower())
    
    def trim_string(self)->'StringBuilder':
        return StringBuilder(self.string.strip())
    
    
    def replace(self, old: str, new: str) -> 'StringBuilder':
        return StringBuilder(self.string.replace(old, new))

    def reverse(self) -> 'StringBuilder':
        return StringBuilder(self.string[::-1])

    def build(self)->str:
        return self.string

if __name__=="__main__":
    s="utsav     a"
    builder=StringBuilder(s)
    string=builder.normalize_spaces().build()
    print(string)
