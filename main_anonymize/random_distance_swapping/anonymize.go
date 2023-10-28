package main

import (
	"flag"
	"fmt"
	"github.com/cheggaaa/pb/v3"
	"labs/library"
	"math/rand"
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
	anonymizedFileName := "anonymized_p.csv"
	swapMappingTuple := make([][]int, rowLength)
	// データのコピーを作成
	anonymizedData := make([][]int, rowLength)
	usedDistanceSum := 0
	usedDistanceHist := make([]int, 9)
	fmt.Println("distanceOrderMax: ", *distanceOrderMax)
	// 各行に対してハミング距離を計算してswap
	isChanged := make([]bool, rowLength)
	bar := pb.StartNew(rowLength)
	for i := 0; i < rowLength; i++ {
		bar.Increment()
		if isChanged[i] {
			continue
		}
		sourceData := make([]int, len(pData[i]))
		sourceData = pData[i]
		distanceOrder := rand.Perm(*distanceOrderMax)
		for _, j := range distanceOrder {
			targetData_index_list := make([]int, 0)
			for k := i + 1; k < rowLength; k++ {
				if isChanged[k] {
					continue
				}
				targetData := pData[k]
				distance := library.HammingDistance(sourceData, targetData)
				if distance == j {
					targetData_index_list = append(targetData_index_list, k)
				}
			}
			if len(targetData_index_list) > 0 {
				targetData_index := targetData_index_list[rand.Intn(len(targetData_index_list))]
				anonymizedData[i] = pData[targetData_index]
				anonymizedData[targetData_index] = pData[i]
				isChanged[i] = true
				isChanged[targetData_index] = true
				usedDistanceSum += j
				usedDistanceHist[j]++
				swapMappingTuple[i] = append(swapMappingTuple[i], targetData_index)
				break
			}
		}
		if !isChanged[i] {
			anonymizedData[i] = pData[i]
			isChanged[i] = true
			usedDistanceSum += 0
			usedDistanceHist[0]++
			swapMappingTuple[i] = append(swapMappingTuple[i], i)
		}
	}
	bar.Finish()

	fmt.Println("usedDistanceSum: ", usedDistanceSum)
	fmt.Println("usedDistanceHist: ", usedDistanceHist)
	fmt.Println("usefullness: ", library.Usefullness(anonymizedData, pData))

	// 結果をCSVファイルに書き込む
	library.Write_data_list_to_csv(anonymizedFileName, anonymizedData)

	// check if sorted in dictionary order is same
	sorted_pData := library.Sort_in_dictionary_order(pData)
	sorted_anonymizedData := library.Sort_in_dictionary_order(anonymizedData)
	for i := 0; i < rowLength; i++ {
		for j := 0; j < len(pData[i]); j++ {
			if sorted_pData[i][j] != sorted_anonymizedData[i][j] {
				fmt.Println("Error: not sorted in dictionary order at ", i, j)
				return
			}
		}
	}

	// read r.csv
	rData := library.Get_data_list_from_csv("r.csv")
	if rData == nil {
		fmt.Println("Error: rData is nil")
		return
	}
	anonymized_rFileName := "anonymized_r.csv"
	anonymizedRData := make([][]int, len(rData))
	// swap using swapMappingTuple

	for i := 0; i < rowLength; i++ {
		if anonymizedRData[i] == nil {

			anonymizedRData[i] = rData[swapMappingTuple[i][0]]
			anonymizedRData[swapMappingTuple[i][0]] = rData[i]
		} else {
			continue
		}
	}
	//fmt.Println("anonymizedRData: ", anonymizedRData)
	// write anonymized_r.csv
	library.Write_data_list_to_csv(anonymized_rFileName, anonymizedRData)
	swapData := make([][]int, rowLength)
	for i := 0; i < rowLength; i++ {
		if swapData[i] == nil {
			swapData[i] = append(swapData[i], i)
			swapData[i] = append(swapData[i], swapMappingTuple[i][0])

			swapData[swapMappingTuple[i][0]] = append(swapData[swapMappingTuple[i][0]], swapMappingTuple[i][0])
			swapData[swapMappingTuple[i][0]] = append(swapData[swapMappingTuple[i][0]], i)
		} else {
			continue
		}
	}
	library.Write_data_list_to_csv("swapMappingTuple.csv", swapData)
}
