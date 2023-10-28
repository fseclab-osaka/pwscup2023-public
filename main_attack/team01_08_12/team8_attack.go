package main

import (
	"fmt"
	"os"

	//"github.com/cheggaaa/pb/v3"
	"labs/library"
)

// maxIgnore: maxIgnore以下の距離のレコードを無視する
func prepareAnswerData(publicData [][]int, teamData [][]int, maxIgnore int) [][]int {
	answerData := make([][]int, 0)
	//bar := pb.StartNew(len(publicData))

	for _, publicRecord := range publicData {
		nearestRecord := library.FindNearestRecord(publicRecord, teamData, maxIgnore)
		answerData = append(answerData, nearestRecord)
		//fmt.Println(nearestRecord)
		//bar.Increment()
	}
	//bar.Finish()
	return answerData
}

func anonymize(x []int) []int {
	new_x := make([]int, len(x))
	for i := 0; i < len(x); i++ {
		switch x[i] {
		case 0:
			new_x[i] = 0
		case 1, 2, 3:
			new_x[i] = 1
		case 4, 5, 6:
			new_x[i] = 4
		case 7, 8, 9:
			new_x[i] = 7
		}
	}
	return new_x

}

func main() {
	publicFile, err := os.Open("p.csv")

	if err != nil {
		fmt.Println(err)
		return
	}
	defer publicFile.Close()

	//teamFileName := "team08_p_sorted.csv"
	teamFileName := "main-atk-public/b_08.csv"

	teamFile, err := os.Open(teamFileName)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer teamFile.Close()
	publicData := library.ReadCSV(publicFile)
	teamData := library.ReadCSV(teamFile)
	answerData := [][]int{}

	for i := 0; i < len(teamData); i++ {
		new_x := anonymize(publicData[i])
		nearestRecord := library.FindNearestRecord(new_x, teamData, -1)
		//fmt.Println(nearestRecord)
		answerData = append(answerData, nearestRecord[8:])
	}

	// write expected r.csv
	// write to csv
	file, err := os.Create("team08_expect_r.csv")
	if err != nil {
		fmt.Println(err)
		return
	}
	defer file.Close()
	for i := 0; i < len(teamData); i++ {
		for j := 0; j < len(answerData[i]); j++ {
			file.Write([]byte(fmt.Sprintf("%d", answerData[i][j])))
			if j != len(answerData[i])-1 {
				file.Write([]byte(fmt.Sprintf(",")))
			}
		}
		file.Write([]byte(fmt.Sprintf("\n")))
	}
}
