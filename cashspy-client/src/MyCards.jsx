import React, { useState, useEffect } from "react";
import axios from "axios";
import Box from "@mui/joy/Box";
import Button from "@mui/joy/Button";
import AddIcon from "@mui/icons-material/Add";
import DialogTitle from "@mui/joy/DialogTitle";
import DialogContent from "@mui/joy/DialogContent";
import ModalDialog from "@mui/joy/ModalDialog";
import {
  CircularProgress,
  Stack,
  Modal,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from "@mui/material";
import FloatingLabelInput from "./input";

export default function MyCards() {
  const [cards, setCards] = useState([]);
  const [banks, setBanks] = useState([]);
  const [bankCards, setBankCards] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedBank, setSelectedBank] = useState("");
  const [selectedCard, setSelectedCard] = useState(0);

  const apiUrl = "http://localhost:8000/api/v1";

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      fetchMyCards(token);
      fetchBanks(token);
    }
  }, []);

  const fetchBanks = async (token) => {
    setLoading(true);
    try {
      const response = await axios.get(`${apiUrl}/banks`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setBanks(response.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchBankCards = async (bankId, token) => {
    setLoading(true);
    try {
      const response = await axios.get(`${apiUrl}/cards?bank_id=${bankId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setBankCards(response.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchMyCards = async (token) => {
    setLoading(true);
    try {
      const response = await axios.get(`${apiUrl}/cards/my`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setCards(response.data);
      console.log(response.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleAddCard = async (cardId, token) => {
    try {
      const response = await axios.post(
        `${apiUrl}/cards/add`,
        {
          card_id: cardId,
        },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      window.location.reload();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleOpenModal = () => setModalOpen(true);
  const handleCloseModal = () => setModalOpen(false);
  const handleBankChange = (event) => {
    const bankId = event.target.value;
    setSelectedBank(bankId);
    fetchBankCards(bankId, localStorage.getItem("token"));
  };
  const handleCardChange = (event) => {
    setSelectedCard(event.target.value);
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

      <Box sx={{ width: "100%", mt: 4 }}>
        <Stack sx={{ gap: 2, width: "100%" }}>
          {error && <div>Error: {error}</div>}
          {cards.map((card) => (
            <Box
              key={card.card_id}
              sx={{ p: 4, backgroundColor: "#f2f3f3", borderRadius: "12px" }}
            >
              {card.card}
            </Box>
          ))}
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
            <DialogTitle>New Card</DialogTitle>
            <DialogContent>Select the options to add new card.</DialogContent>
            <form
              onSubmit={(event) => {
                event.preventDefault();
                handleAddCard(selectedCard, localStorage.getItem("token"));
                handleCloseModal();
              }}
            >
              <Stack spacing={2}>
                <FormControl fullWidth sx={{ mt: 2 }}>
                  <InputLabel id="bank-select-label">Bank</InputLabel>
                  <Select
                    labelId="bank-select-label"
                    id="bank-select"
                    value={selectedBank}
                    label="Bank"
                    onChange={handleBankChange}
                  >
                    {banks.map((bank) => (
                      <MenuItem key={bank.id} value={bank.id}>
                        {bank.name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
                <FormControl fullWidth sx={{ mt: 2 }}>
                  <InputLabel id="card-select-label">Card</InputLabel>
                  <Select
                    labelId="card-select-label"
                    id="card-select"
                    value={selectedCard}
                    label="Card"
                    onChange={handleCardChange}
                  >
                    {bankCards.map((card) => (
                      <MenuItem key={card.id} value={card.id}>
                        {card.name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
                <Button type="submit" sx={{ mt: 2 }} size="lg">
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
