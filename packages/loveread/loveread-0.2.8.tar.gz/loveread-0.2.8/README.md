**This is python module to download books from loveread.ec as txt files**

* Install
`pip3 install loveread`
- Use through terminal
`python3 -m loveread "http://loveread.ec/read_book.php?id=PUT_BOOK_ID"`
* Through code
`import loveread`
`url = "http://loveread.ec/read_book.php?id={PUT_BOOK_ID}`
`loveread.download(url)`

* In both cases the book would appear as txt file in the same folder