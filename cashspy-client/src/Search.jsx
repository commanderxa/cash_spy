import * as React from "react";
import Box from "@mui/joy/Box";
import ListItemDecorator from "@mui/joy/ListItemDecorator";
import Tabs from "@mui/joy/Tabs";
import TabList from "@mui/joy/TabList";
import Tab, { tabClasses } from "@mui/joy/Tab";
import HomeRoundedIcon from "@mui/icons-material/HomeRounded";
import FavoriteBorder from "@mui/icons-material/FavoriteBorder";
import Search from "@mui/icons-material/Search";
import Person from "@mui/icons-material/Person";
import { Stack } from "@mui/material";
import Button from "@mui/joy/Button";
import FloatingLabelInput from "./input";
import MyCards from "./MyCards";

export default function Search() {
  const [item, setItem] = React.useState("");
  const [place, setPlace] = React.useState("");

  const handleSearch = async () => {
    try {
      // Perform a POST request with URL-encoded data
      const response = await axios.get(
        `${apiUrl}/token?=${item}&place=${place}`
      );

      console.log("Response successful", response.data);
    } catch (error) {
      // Handle errors, including those from the API
      alert(
        "Response failed: " + (error.response?.data?.detail || "Unknown error")
      );
    }
  };

  return (
    <Box
      component="form"
      onSubmit={(e) => {
        e.preventDefault();
        handleSearch();
      }}
      sx={{ width: "100%", mt: 4 }}
    >
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
    </Box>
  );
}
