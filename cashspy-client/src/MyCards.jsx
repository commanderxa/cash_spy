import React, { useState, useEffect } from "react";
import axios from "axios";
import Box from "@mui/joy/Box";
import Button from "@mui/joy/Button";
import AddIcon from "@mui/icons-material/Add";
import DialogTitle from "@mui/joy/DialogTitle";
import DialogContent from "@mui/joy/DialogContent";
import FormLabel from "@mui/joy/FormLabel";
import ModalDialog from "@mui/joy/ModalDialog";
import {
  CircularProgress,
  Stack,
  Modal,
  Typography,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from "@mui/material";
import FloatingLabelInput from "./input";

export default function MyCards() {
  const [cards, setCards] = useState([]);
  const [banks, setBanks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedValue, setSelectedValue] = useState("");
  const [inputValue, setInputValue] = useState("");

  const apiUrl = "http://localhost:8000/api/v1";

  const fetchCards = async (token) => {
    setLoading(true);
    try {
      const response = await axios.get(`${apiUrl}/cards`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setCards(response.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchBanks = async (token) => {
    setLoading(true);
    try {
      const response = await axios.get(`${apiUrl}/banks`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setBanks(response.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      fetchCards(token);
      fetchBanks(token);
    }
  }, []);

  const handleOpenModal = () => setModalOpen(true);
  const handleCloseModal = () => setModalOpen(false);
  const handleSelectChange = (event) => setSelectedValue(event.target.value);
  const handleInputChange = (event) => setInputValue(event.target.value);

  const style = {
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    width: 400,
    bgcolor: "background.paper",
    border: "2px solid #000",
    boxShadow: 24,
    p: 4,
  };

  return (
    <>
      {loading && (
        <div
          style={{
            position: "fixed", // Use fixed to cover the entire viewport
            top: 0,
            left: 0,
            width: "100vw",
            height: "100vh",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            backgroundColor: "rgba(255, 255, 255, 0.5)", // Semi-transparent white backdrop
            zIndex: 9999, // High z-index to ensure it's above other content
          }}
        >
          <CircularProgress size="lg" />
        </div>
      )}

      <Box sx={{ width: "100%", mt: 4 }}>
        <Stack sx={{ gap: 2 }}>
          {cards.map((card) => (
            <div key={card.id}>{card.name}</div>
          ))}
          {error && <div>Error: {error}</div>}
          <Button
            sx={{
              position: "fixed",
              bottom: 16,
              left: 0,
              right: 0,
              margin: "0 auto",
            }}
            size="lg"
            variant="solid"
            color="primary"
            startDecorator={<AddIcon />}
            onClick={handleOpenModal}
          >
            Add
          </Button>
        </Stack>

        <Modal open={modalOpen} onClose={handleCloseModal}>
          <ModalDialog>
            <DialogTitle>Create new project</DialogTitle>
            <DialogContent>
              Fill in the information of the project.
            </DialogContent>
            <form
              onSubmit={(event) => {
                event.preventDefault();
                setOpen(false);
              }}
            >
              <Stack spacing={2}>
                <FormControl fullWidth sx={{ mt: 2 }}>
                  <InputLabel id="demo-simple-select-label">Type</InputLabel>
                  <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={selectedValue}
                    label="Type"
                    onChange={handleSelectChange}
                  >
                    <MenuItem value={10}>Option 1</MenuItem>
                    <MenuItem value={20}>Option 2</MenuItem>
                    <MenuItem value={30}>Option 3</MenuItem>
                  </Select>
                </FormControl>
                <FloatingLabelInput
                  label="Name"
                  value={inputValue}
                  onChange={handleInputChange}
                />
                <Button
                  sx={{ mt: 2 }}
                  size="lg"
                  onClick={handleCloseModal} // Assume you might want to close modal after clicking this button
                >
                  Submit
                </Button>
              </Stack>
            </form>
          </ModalDialog>
        </Modal>
      </Box>
    </>
  );
}
