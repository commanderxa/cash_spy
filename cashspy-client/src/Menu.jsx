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

export default function TabsBottomNavExample() {
  const [index, setIndex] = React.useState(0);
  const colors = ["primary"];

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
      sx={{
        flexGrow: 1,
        mt: 4,
        p: 4,
        borderTopLeftRadius: "12px",
        borderTopRightRadius: "12px",
        // bgcolor: `${colors[0]}.500`,
        maxWidth: "400px",
        margin: "0 auto",
      }}
    >
      <Tabs
        size="lg"
        aria-label="Bottom Navigation"
        value={index}
        onChange={(event, value) => setIndex(value)}
        sx={(theme) => ({
          p: 1,
          borderRadius: 16,
          maxWidth: 400,
          mx: "auto",
          border: "1px solid #f2f3f3",
          // boxShadow: theme.shadow.sm,
          "--joy-shadowChannel": theme.vars.palette[colors[0]].darkChannel,
          [`& .${tabClasses.root}`]: {
            py: 1,
            flex: 1,
            transition: "0.3s",
            fontWeight: "md",
            fontSize: "md",
            [`&:not(.${tabClasses.selected}):not(:hover)`]: {
              opacity: 0.7,
            },
          },
        })}
      >
        <TabList
          variant="plain"
          size="sm"
          disableUnderline
          sx={{ borderRadius: "lg", p: 0, gap: 1, }}
        >
          <Tab
            disableIndicator
            orientation="vertical"
            {...(index === 0 && { color: colors[0] })}
          >
            <ListItemDecorator>
              <HomeRoundedIcon />
            </ListItemDecorator>
            My Cards
          </Tab>
          <Tab
            disableIndicator
            orientation="vertical"
            {...(index === 2 && { color: colors[2] })}
          >
            <ListItemDecorator>
              <Search />
            </ListItemDecorator>
            Search
          </Tab>
        </TabList>
      </Tabs>

      {index === 0 && (
        <MyCards />
      )}
      {index === 1 && (
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
      )}
    </Box>
  );
}
