package main

import (
	"fmt"
	"os"

	//"github.com/cheggaaa/pb/v3"
	"labs/library"
)

func main() {
	team_name := "01"

	teamFileName := "main-atk-public/b_" + team_name + ".csv"

	teamFile, err := os.Open(teamFileName)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer teamFile.Close()
	teamData := library.ReadCSV(teamFile)

	duplicationHist := make([]int, len(teamData))
	visited := make([]bool, len(teamData))

	for i := 0; i < len(teamData); i++ {
		if visited[i] {
			continue
		}
		for j := 0; j < len(teamData); j++ {
			if i == j {
				continue
			}
			if visited[j] {
				continue
			}
			if library.HammingDistance(teamData[i][:8], teamData[j][:8]) == 1 {
				duplicationHist[i]++
				visited[j] = true
			}
		}
	}
	for i := 0; i < len(duplicationHist); i++ {
		if duplicationHist[i] > 0 {
			fmt.Println(i, duplicationHist[i])
		}
	}
	len_dup := 0
	for i := 0; i < len(teamData); i++ {
		if duplicationHist[i] > 0 {
			len_dup++
		}
	}
	fmt.Println(len_dup)
	// write to csv
	file, err := os.Create("duplication_" + team_name + ".csv")
	if err != nil {
		fmt.Println(err)
		return
	}
	defer file.Close()
	for i := 0; i < len(teamData); i++ {
		if duplicationHist[i] > 0 {
			file.Write([]byte(fmt.Sprintf("%d,%d\n", i, duplicationHist[i])))
		}
	}
	return
}
