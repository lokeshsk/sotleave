-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 26, 2023 at 06:46 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `leaves`
--

-- --------------------------------------------------------

--
-- Table structure for table `leave_records`
--

CREATE TABLE `leave_records` (
  `ID` int(11) NOT NULL,
  `app_date` date DEFAULT NULL,
  `ename` varchar(200) DEFAULT NULL,
  `eid` int(11) DEFAULT NULL,
  `designation` varchar(50) DEFAULT NULL,
  `department` varchar(50) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `no_days` int(11) DEFAULT NULL,
  `reason` varchar(500) DEFAULT NULL,
  `work_done` varchar(100) DEFAULT NULL,
  `nature` varchar(200) DEFAULT NULL,
  `esign` varchar(100) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `manager` varchar(100) DEFAULT NULL,
  `cleaves` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `leave_records`
--



--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`) VALUES
(1, 'manager', 'c868c25684ea0fa68b8615780ba88de8db6fe0fafd80e992b23ec5b65452efa3'),
(2, 'amogh', '7be3d0434d34dcb911badafb711a6ec595f9cb3abbabd17e481f38b694d33ac2'),
(3, 'lokesh', 'e2e835b33f6c3e57b2a3078d38378dac3fe0fdb5734842e378e95d29fbde0bd6');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `leave_records`
--
ALTER TABLE `leave_records`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `leave_records`
--
ALTER TABLE `leave_records`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=89;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
