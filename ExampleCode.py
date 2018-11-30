import GrammarChecker

myChecker = GrammarChecker.GrammarChecker()
sents = ["A lot of students goes to school today", "after studying, I play video games", "I feel interesting",
         "a basket of pies have disappeared", "John and Henry is best friends"]
# TRY GRAMMAR CHECKER
error_list, error_count = myChecker.find_errors(sents)
GrammarChecker.display_errors(sents, error_list)