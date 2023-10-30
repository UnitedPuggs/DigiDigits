package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/gorilla/mux"
	_ "github.com/mattn/go-sqlite3"
)

type M map[string]interface{}

func main() {
	db, err := sql.Open("sqlite3", "../digidigits.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()
	fmt.Println("Connection made!")

	r := mux.NewRouter()

	r.HandleFunc("/card-info/{card_num}", get_card_info(db)).Methods("GET")

	http.ListenAndServe(":80", r)
}

func get_card_info(db *sql.DB) http.HandlerFunc {
	var card_arr []M
	return func(w http.ResponseWriter, r *http.Request) {
		// cors is silly, this is my workaround for now
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PATCH, PUT, DELETE, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers:", "Origin, Content-Type, X-Auth-Token, Authorization, Accept, Accept-Language")
		w.Header().Set("Content-Type", "application/json")

		vars := mux.Vars(r)
		card_num := vars["card_num"]

		rows, err := db.Query("select * from marketdata where card_num = ? group by card_num, rarity, pack", card_num)
		if err != nil {
			log.Fatal(err)
		}
		defer rows.Close()

		for rows.Next() {
			card := make(map[string]interface{})
			var card_name string
			var card_num string
			var market_price string
			var pack string
			var rarity string
			var date string
			err = rows.Scan(&card_name, &card_num, &market_price, &pack, &rarity, &date)
			if err != nil {
				log.Fatal(err)
			}
			card["card_name"] = card_name
			card["card_num"] = card_num
			card["market_price"] = market_price
			card["pack"] = pack
			card["rarity"] = rarity
			card["date"] = date
			card_arr = append(card_arr, card)
		}
		err = rows.Err()

		if err != nil {
			log.Fatal(err)
		}

		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(card_arr)
		card_arr = nil
	}
}
