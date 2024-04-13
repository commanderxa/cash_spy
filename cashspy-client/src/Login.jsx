import * as React from "react";
import Box from "@mui/joy/Box";
import ListItemDecorator from "@mui/joy/ListItemDecorator";
import Tabs from "@mui/joy/Tabs";
import TabList from "@mui/joy/TabList";
import Tab, { tabClasses } from "@mui/joy/Tab";
import InputIcon from "@mui/icons-material/Input";
import LoginIcon from "@mui/icons-material/Login";
import Input from "@mui/joy/Input";
import Button from "@mui/joy/Button";
import { Stack } from "@mui/material";
import FloatingLabelInput from "./input";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function TabsBottomNavExample() {
  const [index, setIndex] = React.useState(0);
  const [username, setUsername] = React.useState("");
  const [password, setPassword] = React.useState("");

  const navigate = useNavigate();

  const apiUrl = "http://localhost:8000/api/v1/auth";

  const handleLogin = async () => {
    console.log(`${username}: ${password}`);
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    try {
      // Perform a POST request with URL-encoded data
      const response = await axios.post(`${apiUrl}/token`, formData, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      // Store the access token in localStorage and log success
      localStorage.setItem("token", response.data.access_token);
      console.log("Login successful", response.data);

      window.location.reload();
    } catch (error) {
      // Handle errors, including those from the API
      alert(
        "Login failed: " + (error.response?.data?.detail || "Unknown error")
      );
    }
  };

  const handleRegister = async () => {
    if (password !== repeatPassword) {
      alert("Passwords don't match");
      return;
    }
    try {
      const response = await axios.post(`${apiUrl}/register`, {
        username: username,
        password: password,
      });
      localStorage.setItem("token", response.data.access_token);
      console.log("Registration successful", response.data);
    } catch (error) {
      alert("Registration failed: " + error.response.data.detail);
    }
  };

  const colors = ["primary"];
  return (
    <Box
      sx={{
        maxWidth: "400px",
        margin: "0 auto",
        p: 4,
        borderTopLeftRadius: "12px",
        borderTopRightRadius: "12px",
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
          boxShadow: theme.shadow.sm,
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
          sx={{ borderRadius: "lg", p: 0 }}
        >
          <Tab
            disableIndicator
            orientation="vertical"
            {...(index === 0 && { color: colors[0] })}
          >
            <ListItemDecorator>
              <LoginIcon />
            </ListItemDecorator>
            Login
          </Tab>
          <Tab
            disableIndicator
            orientation="vertical"
            {...(index === 1 && { color: colors[0] })}
          >
            <ListItemDecorator>
              <InputIcon />
            </ListItemDecorator>
            Register
          </Tab>
        </TabList>
      </Tabs>

      {index === 0 && (
        <Box
          component="form"
          onSubmit={(e) => {
            e.preventDefault();
            handleLogin();
          }}
          sx={{ width: "100%", mt: 4 }}
        >
          <Stack sx={{ gap: 2 }}>
            <FloatingLabelInput
              label="Username"
              placeholder="mister"
              onChange={(e) => setUsername(e.target.value)}
            />
            <FloatingLabelInput
              label="Password"
              placeholder="*******"
              type="password"
              onChange={(e) => setPassword(e.target.value)}
            />
            <Button type="submit" sx={{ marginTop: 2, p: 2 }}>
              Login
            </Button>
          </Stack>
        </Box>
      )}
      {index === 1 && (
        <Box
          component="form"
          onSubmit={(e) => {
            e.preventDefault();
            handleRegister();
          }}
          sx={{ width: "100%", mt: 4 }}
        >
          <Stack sx={{ gap: 2 }}>
            <FloatingLabelInput
              label="Username"
              placeholder="mister"
              onChange={(e) => setUsername(e.target.value)}
            />
            <FloatingLabelInput
              label="Password"
              placeholder="*******"
              type="password"
              onChange={(e) => setPassword(e.target.value)}
            />
            <Button type="submit" sx={{ marginTop: 2, p: 2 }}>
              Register
            </Button>
          </Stack>
        </Box>
      )}
    </Box>
  );
}
