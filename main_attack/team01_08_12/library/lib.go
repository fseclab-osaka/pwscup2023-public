package library

import (
	"encoding/csv"
	"fmt"
	"io"
	"os"
	"sort"
	"strconv"
)

func Usefullness(data [][]int, publicdata [][]int) float64 {
	fixed := 0
	for i := 0; i < len(data); i++ {
		for j := 0; j < len(data[i]); j++ {
			if data[i][j] != publicdata[i][j] {
				fixed++
			}
		}
	}
	return 1  - (float64(fixed) / (float64(len(data))*float64(18)))
}

func HammingDistance(s1, s2 []int) int {
	if len(s1) != len(s2) {
		return -1 // 長さが異なる場合エラーを返す
	}
	distance := 0
	for i := range s1 {
		if s1[i] != s2[i] {
			distance++
		}
	}
	return distance
}

func Sort_in_dictionary_order(data [][]int) [][]int {
	sort.Slice(data, func(i, j int) bool {
		for k := 0; k < len(data[i]); k++ {
			if data[i][k] != data[j][k] {
				return data[i][k] < data[j][k]
			}
		}
		return false
	})
	return data
}


func Get_data_list_from_csv(filename string) [][]int {
	// ファイルを開く
	pFile, err := os.Open(filename)
	if err != nil {
		fmt.Println("Error opening input file:", err)
		return nil
	}
	defer pFile.Close()

	// CSVリーダーを作成
	reader := csv.NewReader(pFile)

	// データを読み込む
	pData, err := reader.ReadAll()
	if err != nil {
		fmt.Println("Error reading input:", err)
		return nil
	}
	// pData to int_pData
	int_pData := make([][]int, len(pData))
	for i, row := range pData {
		for _, val := range row {
			int_pData[i] = append(int_pData[i], atoi(val))
		}
	}
	return int_pData
}

func Write_data_list_to_csv(filename string, data [][]int) {
	anonymizedFile, err := os.Create(filename)
	if err != nil {
		fmt.Println("Error creating output file:", err)
		return
	}
	defer anonymizedFile.Close()

	anonymizedWriter := csv.NewWriter(anonymizedFile)
	defer anonymizedWriter.Flush()

	for _, row := range data {
		stringRow := make([]string, len(row))
		for i, val := range row {
			stringRow[i] = itoa(val)
		}
		if err := anonymizedWriter.Write(stringRow); err != nil {
			fmt.Println("Error writing row:", err)
			return
		}
	}
}


func atoi(s string) int {
	result := 0
	for _, c := range s {
		result = result*10 + int(c-'0')
	}
	return result
}

func itoa(n int) string {
	if n == 0 {
		return "0"
	}
	result := ""
	for n > 0 {
		digit := n % 10
		result = string('0'+digit) + result
		n /= 10
	}
	return result
}


// maxIgnore: maxIgnore以下の距離のレコードを無視する. pとrを合わせた一行ぶんのデータを返す
func FindNearestRecord(sourceRecord []int, objectRecords [][]int, maxIgnore int) []int {
	minDistance := -1
	var nearestRecord []int

	for _, objectRecord := range objectRecords {
		distance := HammingDistance(sourceRecord, objectRecord[0:8])
		if distance <= maxIgnore {
			//fmt.Println("distance is 0")
			continue
		}
		if minDistance == -1 || distance < minDistance {
			minDistance = distance
			nearestRecord = objectRecord
		}
	}
	if minDistance == -1 {
		fmt.Println("no record found")
		// ten 0 record
		nearestRecord = make([]int, 18)
		for i := 0; i < 18; i++ {
			nearestRecord[i] = 0
		}
	}

	return nearestRecord
}


func ReadCSV(file *os.File) [][]int {
	var data [][]int
	reader := csv.NewReader(file)

	for {
		record, err := reader.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			fmt.Println(err)
			break
		}

		recordInt := make([]int, len(record))
		for i, value := range record {
			intValue, _ := strconv.Atoi(value)
			recordInt[i] = intValue
		}

		data = append(data, recordInt)
	}
	return data
}


func WriteCSV(data [][]int, fileName string) {
	file, err := os.Create(fileName)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	for _, record := range data {
		recordStrings := make([]string, len(record))
		for i, value := range record {
			recordStrings[i] = strconv.Itoa(value)
		}
		err := writer.Write(recordStrings)
		if err != nil {
			fmt.Println(err)
			return
		}
	}

}