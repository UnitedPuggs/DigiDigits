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

type market struct {
	id           string
	market_price float64
	date         string
}

func main() {
	db, err := sql.Open("sqlite3", "../digidigits.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()
	fmt.Println("Connection made!")

	r := mux.NewRouter()

	r.HandleFunc("/cards/{card_num}", get_card(db)).Methods("GET")
	r.HandleFunc("/cards/info/{card_id}", get_card_info(db)).Methods("GET")
	r.HandleFunc("/cards/market/{card_id}", get_card_market_data(db)).Methods("GET")

	http.ListenAndServe(":80", r)
}

func get_card_info(db *sql.DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		var card_arr []M
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PATCH, PUT, DELETE, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers:", "Origin, Content-Type, X-Auth-Token, Authorization, Accept, Accept-Language")
		w.Header().Set("Content-Type", "application/json")

		vars := mux.Vars(r)
		card_id := vars["card_id"]

		rows, err := db.Query("select * from digimon_card_data where id = ? group by card_num, rarity, pack", card_id)
		if err != nil {
			log.Fatal(err)
		}
		defer rows.Close()

		for rows.Next() {
			var card_name string
			var card_num string
			var market_price string
			var pack string
			var rarity string
			var date string
			var id string
			err = rows.Scan(&card_name, &card_num, &market_price, &pack, &rarity, &date, &id)
			if err != nil {
				log.Fatal(err)
			}

			card := map[string]interface{}{"card_name": card_name, "card_num": card_num, "market_price": market_price, "pack": pack, "rarity": rarity, "date": date, "id": id}
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

func get_card(db *sql.DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		var card_arr []M
		// cors is silly, this is my workaround for now
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PATCH, PUT, DELETE, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers:", "Origin, Content-Type, X-Auth-Token, Authorization, Accept, Accept-Language")
		w.Header().Set("Content-Type", "application/json")

		vars := mux.Vars(r)
		card_num := vars["card_num"]

		rows, err := db.Query("select * from digimon_card_data where card_name like '%' || ? || '%' group by card_num, rarity, pack", card_num)
		if err != nil {
			log.Fatal(err)
		}
		defer rows.Close()

		for rows.Next() {
			var card_name string
			var card_num string
			var market_price string
			var pack string
			var rarity string
			var date string
			var id string
			err = rows.Scan(&card_name, &card_num, &market_price, &pack, &rarity, &date, &id)
			if err != nil {
				log.Fatal(err)
			}

			card := map[string]interface{}{"card_name": card_name, "card_num": card_num, "market_price": market_price, "pack": pack, "rarity": rarity, "date": date, "id": id}
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

func get_card_market_data(db *sql.DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		var card_arr []M
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PATCH, PUT, DELETE, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers:", "Origin, Content-Type, X-Auth-Token, Authorization, Accept, Accept-Language")
		w.Header().Set("Content-Type", "application/json")

		vars := mux.Vars(r)
		card_id := vars["card_id"]

		rows, err := db.Query("select id, market_price, date from card_market_data where id = ? order by date desc", card_id)
		if err != nil {
			log.Fatal(err)
		}
		defer rows.Close()

		for rows.Next() {
			//card := make(map[string]interface{})
			var id string
			var market_price float64
			var date string

			err = rows.Scan(&id, &market_price, &date)
			if err != nil {
				log.Fatal(err)
			}
			card := map[string]interface{}{"id": id, "market_price": market_price, "date": date}

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
