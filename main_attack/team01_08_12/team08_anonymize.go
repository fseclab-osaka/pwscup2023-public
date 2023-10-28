package main

import (
	"flag"
	"fmt"
	"github.com/cheggaaa/pb/v3"
	"labs/library"
)

func main() {
	// 公開データ
	// command flag
	// distanceOrderMax
	input_file_name := flag.String("input", "p.csv", "input file name")
	distanceOrderMax := flag.Int("max", 9, "max distance order")
	flag.Parse()
	pData := library.Get_data_list_from_csv(*input_file_name)
	rowLength := len(pData)
	if pData == nil {
		fmt.Println("Error: pData is nil")
		return
	}
	anonymizedFileName := "team08_p.csv"
	// データのコピーを作成
	anonymizedData := make([][]int, rowLength)
	fmt.Println("distanceOrderMax: ", *distanceOrderMax)
	bar := pb.StartNew(rowLength)
	for i := 0; i < rowLength; i++ {
		for j := 0; j < len(pData[i]); j++ {
			switch pData[i][j] {
			case 0:
				anonymizedData[i] = append(anonymizedData[i], 0)
			case 1, 2, 3:
				anonymizedData[i] = append(anonymizedData[i], 1)
			case 4, 5, 6:
				anonymizedData[i] = append(anonymizedData[i], 4)
			case 7, 8, 9:
				anonymizedData[i] = append(anonymizedData[i], 7)
			}
		}
	}
	bar.Finish()

	// 結果をCSVファイルに書き込む
	r_data := library.Get_data_list_from_csv("r.csv")
	// concat r_data and anonymizedData
	for i := 0; i < rowLength; i++ {
		for j := 0; j < len(r_data[i]); j++ {
			anonymizedData[i] = append(anonymizedData[i], r_data[i][j])
		}
	}

	library.Write_data_list_to_csv(anonymizedFileName, anonymizedData)

}
