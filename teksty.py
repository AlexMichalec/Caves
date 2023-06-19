intro = """
        CCCCCCCCCCCCC                                                                                          
     CCC::::::::::::C                                                                                          
   CC:::::::::::::::C                                                                                         
  C:::::CCCCCCCC::::C                                                                                         
 C:::::C       CCCCCC    aaaaaaaaaaaaa    vvvvvvv           vvvvvvv     eeeeeeeeeeee          ssssssssss   
C:::::C                  a::::::::::::a    v:::::v         v:::::v    ee::::::::::::ee      ss::::::::::s  
C:::::C                  aaaaaaaaa:::::a    v:::::v       v:::::v    e::::::eeeee:::::ee  ss:::::::::::::s 
C:::::C                           a::::a     v:::::v     v:::::v    e::::::e     e:::::e  s::::::ssss:::::s
C:::::C                    aaaaaaa:::::a      v:::::v   v:::::v     e:::::::eeeee::::::e   s:::::s  ssssss 
C:::::C                  aa::::::::::::a       v:::::v v:::::v      e:::::::::::::::::e      s::::::s      
C:::::C                 a::::aaaa::::::a        v:::::v:::::v       e::::::eeeeeeeeeee          s::::::s   
 C:::::C       CCCCCC  a::::a    a:::::a         v:::::::::v        e:::::::e             ssssss   s:::::s 
  C:::::CCCCCCCC::::C  a::::a    a:::::a          v:::::::v         e::::::::e            s:::::ssss::::::s
   CC:::::::::::::::C  a:::::aaaa::::::a           v:::::v           e::::::::eeeeeeee    s::::::::::::::s 
     CCC::::::::::::C   a::::::::::aa:::a           v:::v             ee:::::::::::::e     s:::::::::::ss  
        CCCCCCCCCCCCC    aaaaaaaaaa  aaaa            vvv                eeeeeeeeeeeeee      sssssssssss     
                                                                                            by Alex Michalec"""

intro1 = intro.split(sep="\n")
intro1 = [x[0:23] for x in intro1]
intro1 = "\n".join(intro1)

temp = intro.split(sep="\n")
temp = [" "*22+ x[23:40] for x in temp]
intro2 = "\n".join(temp)

temp = intro.split(sep="\n")
temp = [" "*40+ x[41:67] for x in temp]
intro3 = "\n".join(temp)

temp = intro.split(sep="\n")
temp = [" "*67+ x[68:90] for x in temp]
intro4 = "\n".join(temp)

temp = intro.split(sep="\n")
temp = [" "*89+ x[90:] for x in temp]
temp[len(temp)-1] = ""
intro5 = "\n".join(temp)

intros = [intro1, intro2, intro3, intro4, intro5]



