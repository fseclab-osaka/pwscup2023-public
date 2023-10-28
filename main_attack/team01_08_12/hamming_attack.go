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

func main() {
	team_name := "12"

	publicFile, err := os.Open("p.csv")

	if err != nil {
		fmt.Println(err)
		return
	}
	defer publicFile.Close()

	teamFileName := "main-atk-public/b_" + team_name + ".csv"

	teamFile, err := os.Open(teamFileName)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer teamFile.Close()
	publicData := library.ReadCSV(publicFile)
	teamData := library.ReadCSV(teamFile)

	answerData := make([][]int, 0)

	for _, publicRecord := range publicData {
		nearestRecord := library.FindNearestRecord(publicRecord, teamData, 0)
		answerData = append(answerData, nearestRecord[8:])
	}
	// write answerData to file
	library.Write_data_list_to_csv("attack_result/"+"team"+team_name+"_expect_r.csv", answerData)

}
