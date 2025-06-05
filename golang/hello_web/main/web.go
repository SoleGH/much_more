package main

import (
	"fmt"
	"net/http"
	"strings"
)

func hello(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()
	fmt.Println(r.Form)
	fmt.Println("path", r.URL.Path)
	fmt.Println("scheme", r.URL.Scheme)
	fmt.Println(r.Form["url_long"])
	for k, v := range r.Form {
		fmt.Println("key:", k)
		fmt.Println("val:", strings.Join(v, ""))
	}
	fmt.Fprintf(w, "hello as")
}

// func main() {
// 	http.HandleFunc("/", hello)
// 	err := http.ListenAndServe(":9090", nil)
// 	if err != nil {
// 		log.Fatal("ListenAndServer", err)
// 	}
// }
