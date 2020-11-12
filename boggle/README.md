## A simple boggle solver

```
Usage: boggle.py [OPTIONS]

Options:
  -i, --input_file TEXT         input file representing a boggle board
                                [required]
  -d, --dictionary_file TEXT    dictionary file to search against  [required]
  -l, --minimum_length INTEGER  only return words longer than this
  --help                        Show this message and exit.
  ```

##  Example
Given a boggle board, return a list of words at least 5 characters long in the dictionary, 
with trace positions.


  ```python
  python boggle.py -i board.example -d words_alpha.txt -l 5

1 : prelim  -> (2,1)(1,0)(0,1)(0,2)(1,3)(0,3)
2 : crile  -> (2,3)(2,2)(1,3)(0,2)(0,1)
3 : miler  -> (0,3)(1,3)(0,2)(0,1)(1,0)
4 : relic  -> (1,0)(0,1)(0,2)(1,3)(2,3)

  ```