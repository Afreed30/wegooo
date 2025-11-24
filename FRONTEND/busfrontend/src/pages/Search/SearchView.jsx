import React, { useState } from "react";
import "./search.css";

export default function SearchView({ onSearch }) {
  const [origin, setOrigin] = useState("");
  const [destination, setDestination] = useState("");
  const [date, setDate] = useState("");

  const today = new Date().toISOString().split("T")[0];
  const cities = [
    "Adilabad", "Bhadradri Kothagudem", "Hanumakonda", "Hyderabad", "Jagtial",
    "Jangaon", "Jayashankar Bhupalpally", "Jogulamba Gadwal", "Kamareddy",
    "Karimnagar", "Khammam", "Kumuram Bheem Asifabad", "Mahabubabad",
    "Mahabubnagar", "Mancherial", "Medak", "Medchal–Malkajgiri", "Mulugu",
    "Nagarkurnool", "Nalgonda", "Narayanpet", "Nirmal", "Nizamabad",
    "Peddapalli", "Rajanna Sircilla", "Ranga Reddy", "Sangareddy", "Siddipet",
    "Suryapet", "Vikarabad", "Wanaparthy", "Warangal", "Yadadri Bhuvanagiri",
    "Alluri Sitharama Raju", "Anakapalli", "Ananthapuramu", "Annamayya", "Bapatla",
    "Chittoor", "Dr. B.R. Ambedkar Konaseema", "East Godavari", "Eluru", "Guntur",
    "Kakinada", "Krishna", "Kurnool", "Nandyal", "NTR", "Palnadu",
    "Parvathipuram Manyam", "Prakasam", "Sri Potti Sriramulu Nellore",
    "Sri Sathya Sai", "Srikakulam", "Tirupati", "Visakhapatnam", "Vizianagaram",
    "West Godavari", "YSR Kadapa"
  ];
  const autoFill = (value) => {
    const match = cities.find((city) =>
      city.toLowerCase().startsWith(value.toLowerCase())
    );
    return match || value; 
  };
  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();

        const selectedDate = new Date(date);
        const todayDate = new Date();
        todayDate.setHours(0, 0, 0, 0);

        // ❌ Past date safety check
        if (selectedDate < todayDate) {
          onSearch(origin, destination, []);
          return;
        }

        onSearch(origin, destination, date);
      }}
      className="search-box"
    >
      <h2 className="search-title">Search Buses</h2>

      <input
        className="search-input"
        list="citieslist"
        placeholder="From"
        onChange={(e) => setOrigin(e.target.value)}
        required
      />
      <input
        className="search-input"
        list="citieslist"
        placeholder="To"
        onChange={(e) => setDestination(e.target.value)}
        required
      />
      <datalist id="citieslist">
        {cities.map((city, index) => (
          <option key={index} value={city} />
        ))}
      </datalist>
      <input
        type="date"
        className="search-input"
        min={today}   
        onChange={(e) => setDate(e.target.value)}
        required
      />

      <button className="search-btn">Search</button>
    </form>
  );
}
