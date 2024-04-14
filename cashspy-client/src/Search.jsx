import * as React from "react";
import Box from "@mui/joy/Box";
import Search from "@mui/icons-material/Search";
import { Stack, CircularProgress } from "@mui/material";
import Button from "@mui/joy/Button";
import FloatingLabelInput from "./input";
import axios from "axios";
import { useState } from "react";

export default function SearchTab() {
  const [place, setPlace] = useState("");
  const [item, setItem] = useState("");
  const [offers, setOffers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchOffers = async () => {
    const apiUrl = "http://localhost:8000/api/v1";
    const token = localStorage.getItem("token"); // Assuming the token is stored in localStorage
    setLoading(true);
    try {
      console.log(item);
      const response = await axios.get(`${apiUrl}/offers/best`, {
        params: {
          place: place,
          item: item,
        },
        headers: { Authorization: `Bearer ${token}` },
      });
      setOffers(response.data);
    } catch (error) {
      console.error("Fetching offers failed:", error);
      setError("Failed to fetch offers");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {loading && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100vw",
            height: "100vh",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            backgroundColor: "rgba(255, 255, 255, 0.5)",
            zIndex: 9999,
          }}
        >
          <CircularProgress size="lg" />
        </div>
      )}
      <Box
        component="form"
        onSubmit={(e) => {
          fetchOffers();
          e.preventDefault();
        }}
        sx={{ width: "100%", mt: 4 }}
      >
        <Stack sx={{ gap: 4 }}>
          <Stack sx={{ gap: 2 }}>
            <FloatingLabelInput
              label="Предмет"
              placeholder="Ноутбук"
              onChange={(e) => setItem(e.target.value)}
            />
            <FloatingLabelInput
              label="Место"
              placeholder="Технодом"
              onChange={(e) => setPlace(e.target.value)}
            />
            <Button type="submit" sx={{ marginTop: 2, p: 2 }}>
              Search
            </Button>
          </Stack>
          <Stack sx={{ gap: 2 }}>
            {offers.map((offer) => (
              <Stack
                key={offer.offer_id}
                sx={{ p: 4, backgroundColor: "#f2f3f3", borderRadius: "12px" }}
                direction="row"
                justifyContent="space-between"
                alignItems="center"
              >
                <b>{offer.name}</b>
                {offer.cashback}%
              </Stack>
            ))}
          </Stack>
        </Stack>
      </Box>
    </>
  );
}
