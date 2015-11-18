Simple substitution - https://en.wikipedia.org/wiki/Flag_semaphore
ASCII art generated using http://www.ioccc.org/2000/anderson.c (Winner of the obfuscated C contest 2000.)

Could go character by character and associate the flag position with characters

*[master][Counting-Semaphores]$ cat out.txt                                
              <>                                   <>                    
   ()_      ()/      ()       ()    {   ()_      ()/      ()       ()    
  |^^ []   /^^      /^^|     |^^\  {   |^^ []   /^^      /^^|     |^^\   
  [][     <>][     <>][]     [][<>  {  [][     <>][     <>][]     [][<>  

               <>  <>                          <>                   <> []            
        ()_     \()/      ()           ()_     _\)      _()_         \()|     _()    
       |^^ []    ^^      /^^\         |^^ [] [] ^^    [] ^^ []        ^^    [] /^    
  ____ [][       ][     <>][<>  ____  [][       ][       ][    ____   ][      <>[    

     <>          <>              <>          <>       <>                    
   ()/          (/_     _()      _\)       ()/      ()/          ()_      ()    
  |^^           ^^ [] [] /^    [] ^^      /^^      |^^          |^^ []   /^^|   
  [][    ____   ][      <>[       ][     <>][      [][   ____   [][     <>][]   

           []          <>   <>               
   ()_     |()       ()/     \()_   }
  /^^ []    /^      /^^       ^^ []  }
 <>][      <>[     <>][       ][    }

*[master][Counting-Semaphores]$ ./a.out    
warning: this program uses gets(), which is unsafe.
flag{flag_fun_for_the_whole_family}
              <>                                  <>                    
   ()_      ()/      ()       ()       ()_      ()/      ()       ()    
  |^^ []   /^^      /^^|     |^^\     |^^ []   /^^      /^^|     |^^\   
  [][     <>][     <>][]     [][<>    [][     <>][     <>][]     [][<>  

          <>  <>                      <>               <> []            
   ()_     \()/      ()       ()_     _\)      _()_     \()|     _()    
  |^^ []    ^^      /^^\     |^^ [] [] ^^    [] ^^ []    ^^    [] /^    
  [][       ][     <>][<>    [][       ][       ][       ][      <>[    

     <>      <>              <>          <>       <>                    
   ()/      (/_     _()      _\)       ()/      ()/      ()_      ()    
  |^^       ^^ [] [] /^    [] ^^      /^^      |^^      |^^ []   /^^|   
  [][       ][      <>[       ][     <>][      [][      [][     <>][]   

           []          <>   <>               
   ()_     |()       ()/     \()_      ()    
  /^^ []    /^      /^^       ^^ []   |^^|   
 <>][      <>[     <>][       ][      [][]   

^C
*[master][Counting-Semaphores]$ 

