package main

import (
	"fmt"
	"github.com/cheggaaa/pb/v3"
	"labs/library"
	"os"
)

func prepareAnswerData(publicData [][]int, teamData [][]int) [][]int {
	answerData := make([][]int, 0)
	bar := pb.StartNew(len(publicData))

	for _, publicRecord := range publicData {
		nearestRecord := library.FindNearestRecord(publicRecord, teamData, -1)
		answerData = append(answerData, nearestRecord)
		bar.Increment()
	}
	bar.Finish()
	return answerData
}

func main() {
	attack_file, err := os.Open("team08_expect_r.csv")
	if err != nil {
		fmt.Println(err)
		return
	}
	answer_file, err := os.Open("r.csv")
	if err != nil {
		fmt.Println(err)
		return
	}

	attack_data := library.ReadCSV(attack_file)

	answer_data := library.ReadCSV(answer_file)
	// check if answer and attack is same
	different_count := 0
	for i := 0; i < len(attack_data); i++ {
		for j := 0; j < len(attack_data[i]); j++ {
			if attack_data[i][j] != answer_data[i][j] {
				different_count++
			}
		}
	}
	fmt.Println("different_count:", different_count)
	row_different_count := 0
	for i := 0; i < len(attack_data); i++ {
		for j := 0; j < len(attack_data[i]); j++ {
			if attack_data[i][j] != answer_data[i][j] {
				row_different_count++
				break
			}
		}
	}
	fmt.Println("row_different_count:", row_different_count)
	fmt.Println("attack success ratio:", 1-float64(different_count)/float64(len(attack_data)*len(attack_data[0])))

}
