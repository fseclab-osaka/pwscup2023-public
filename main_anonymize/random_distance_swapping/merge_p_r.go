package main

import (
	"fmt"

	"labs/library"
	"os"
)

func main() {

	ano_r, err := os.Open("r.csv")
	if err != nil {
		fmt.Println(err)
		return
	}
	public_file, err := os.Open("anonymized_p.csv")
	if err != nil {
		fmt.Println(err)
		return
	}
	// merge ano_r and public_file
	ano_r_data := library.ReadCSV(ano_r)
	public_data := library.ReadCSV(public_file)
	merged_data := make([][]int, len(ano_r_data))
	for i, _ := range ano_r_data {
		merged_data[i] = append(public_data[i], ano_r_data[i]...)
	}
	// write merged_data to merged_r.csv
	library.WriteCSV(merged_data, "anonymized.csv")
}
