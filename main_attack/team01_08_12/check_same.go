package main

import (
	"fmt"

	"flag"
	"labs/library"
)

func main() {
	// 公開データ
	// command flag
	// distanceOrderMax
	input_file_name := flag.String("input", "main-atk-public/b_08.csv", "input file name")
	flag.Parse()
	pData := library.Get_data_list_from_csv(*input_file_name)
	rowLength := len(pData)
	team12_pData := library.Get_data_list_from_csv("team08_p_sorted.csv")

	for i := 0; i < rowLength; i++ {
		for j := 0; j < 8; j++ {
			if pData[i][j] != team12_pData[i][j] {
				print(i)
				fmt.Println("not same")
				return
			}
		}
	}
	fmt.Println("same")
}
