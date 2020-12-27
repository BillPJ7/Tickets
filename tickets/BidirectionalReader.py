'''
I do not like them in a box
I do not like them (with a fox).
I do not like them in a house
I don't "like them", he said... with a mouse.
I do not like them here or there
I do not, like them anywhere,
I do not like (green eggs and ham
I do not like) them Sam-I-am.  I don't like eggs for one thing.  But green, no way.
'''

#don't declare anything, it becomes what it is when you use it
#this function has to go before the call or it's undefined
 
def NextLine(line):
   #the following is an optional docstring (see print statement at end)
   '''
Take a line, return list[Words,IsSentence]
   '''
   sections = [] #empty list of anythings, mixed type, could be multidimentional
   line = line.rstrip('\n')
   sections.append(line)
   if line == '':
      sections.append(0)
   else:
      sections.append(1)
   return sections 

def ReversePunctuate(word):
   if word == '': #this will handle 2nd space after period
      return word
   parend = '' #these will go 
   quote = ''  #at the end of the word
   if word[0] == '(':
      parend = ')' #flip it
      word = word[1:] #from word[1] on, removes the (
   if word[0] == '\"': #escape character needed
      quote = '\"'
      word = word[1:]
   if len(word) > 2: #cases where 3 punctuations follow a word
      s = word[-3] + word[-2] + word[-1] #last 3 chars
      if s == '...':
         return s + word[:-3] + parend + quote #:-3 means all but last 3
   if len(word) > 1: #cases where 2 punctuations follow a word
       s = word[-2] + word[-1] #last 2 chars
       if s == ').':
          return '.(' + word[:-2] + parend + quote #:-2 means all but last 2
       if s == '\".':
          return '.\"' + word[:-2] + parend + quote
       if s == '\",':
          return ',\"' + word[:-2] + parend + quote
   s = word[-1] #cases where 1 punctuation follows a word
   if s == ')':
      return '(' + word[:-1] + parend + quote
   if s in['.','\"',',','?','!',':']: #nice alternative to or
      return s + word[:-1] + parend + quote
   return word + parend + quote #no trailing punctuation found

#program starts here      
#this will open a file, read into list, close !
with open('In.txt', 'r', encoding = 'utf-8') as f:
   content = f.readlines()
#using with to open a file will auto close it   
with open('Out.txt', 'w', encoding = 'utf-8') as f:
   reverse = -1 #false
   for line in content:
      line = NextLine(line)
      if line[1] == 0: #not a sentence
         f.write(line[0] + '\n')
      else:
         if reverse > 0: #true
            words = line[0].split(' ') #list from space delimited string
            words = words[::-1] #reverse a list
            i = 0
            for word in words:
               words[i] = ReversePunctuate(word)
               i += 1
            line[0] = ' '.join(words) #space delimited string from string list
         f.write(line[0] + '\n') #with lead and trail junk
         reverse *= -1

#what does LineTo Words do?
print(NextLine.__doc__)

'''
I do not like them in a box
.(fox a with) them like not do I
I do not like them in a house
.mouse a with "them like" don't I
I do not like them here or there
,anywhere them like ,not do I
I do not like (green eggs and ham
Sam-I-am them (like not do I
'''
