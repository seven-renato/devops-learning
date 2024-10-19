package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"os/exec"
	"time"
)

type Response struct {
	Message string `json:"message,omitempty"`
	Error   string `json:"error,omitempty"`
}

func dumpHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	password := os.Getenv("PGPASSWORD")
	host := os.Getenv("DB_HOST")
	port := os.Getenv("DB_PORT")
	username := os.Getenv("DB_USER")
	dbName := os.Getenv("DB_NAME")

	timestamp := time.Now().Format("02_01_2006_15_04_05")

	println(timestamp)

	backupPath := fmt.Sprintf("/backup/backup_db_%s.dump", timestamp)

	cmd := exec.Command("docker", "run", "--rm",
		"-e", fmt.Sprintf("PGPASSWORD=%s", password),
		"-e", "PGSSLMODE=require",
		"-v", "/backup/:/backup",
		"postgres:16",
		"pg_dump", "-h", host, "-p", port, "-U", username, "-d", dbName, "-F", "c", "-f", backupPath,
	)

	output, err := cmd.CombinedOutput()
	if err != nil {
		response := Response{
			Error: fmt.Sprintf("Error executing pg_dump: %s\nOutput: %s", err, string(output)),
		}
		w.WriteHeader(http.StatusInternalServerError)
		json.NewEncoder(w).Encode(response)
		return
	}

	response := Response{
		Message: "Backup successful",
	}
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(response)
}

func main() {
	http.HandleFunc("/dump", dumpHandler)
	fmt.Println("Server is running on port 5000...")
	fmt.Println(os.Getwd())

	if err := http.ListenAndServe(":5000", nil); err != nil {
		fmt.Println("Error starting server:", err)
	}
}
