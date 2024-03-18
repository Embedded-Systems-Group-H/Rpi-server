import { useState } from "react";
import {
  Button,
  Modal as BaseModal,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from "@mui/material";
import { styled } from '@mui/system';

import MapboxComponent from "./Map";

interface Entry {
  date: string;
  duration: string;
  distance: string;
  steps: string;
  calories: string;
  coordinates: number[][];
}

interface BasicTableProps {
  entries: Entry[];
}

const Modal = styled(BaseModal)`
  position: fixed;
  z-index: 1300;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const BasicTable = ({ entries }: BasicTableProps) => {
  const [coordinates, setCoordinates] = useState<number[][]>([]);
  const [open, setOpen] = useState<boolean>(false);
  
  const handleOpen = (data: number[][]) => (event: any) => {
    event.preventDefault();
    setCoordinates(data);
    setOpen(true);
  };
  const handleClose = () => setOpen(false);

  return (
    <>
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell align="center">Date</TableCell>
              <TableCell align="center">Duration</TableCell>
              <TableCell align="center">Distance</TableCell>
              <TableCell align="center">Steps</TableCell>
              <TableCell align="center">Calories</TableCell>
              <TableCell align="center">Route</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {entries.map((entry) => (
              <TableRow>
                <TableCell align="center">{entry.date}</TableCell>
                <TableCell align="center">{entry.duration}</TableCell>
                <TableCell align="center">{entry.distance}</TableCell>
                <TableCell align="center">{entry.steps}</TableCell>
                <TableCell align="center">{entry.calories}</TableCell>
                <TableCell align="center">
                  <Button onClick={handleOpen(entry.coordinates)}>
                    Show route
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      {coordinates.length > 0 && (
        <Modal open={open} onClose={handleClose}>
          <MapboxComponent coordinates={coordinates} />
        </Modal>
      )}
    </>
  );
};

export default BasicTable;
