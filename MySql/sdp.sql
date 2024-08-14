-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 14, 2024 at 06:47 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sdp`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `nickname` varchar(50) NOT NULL,
  `age` int(2) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `nickname`, `age`, `email`, `password`) VALUES
(1, 'boon888', 11, '1@gmail.com', '1');

-- --------------------------------------------------------

--
-- Table structure for table `player`
--

CREATE TABLE `player` (
  `id` int(11) NOT NULL,
  `nickname` varchar(50) NOT NULL,
  `age` int(2) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `player`
--

INSERT INTO `player` (`id`, `nickname`, `age`, `email`, `password`) VALUES
(2, 'booo888', 11, '1@gmail.com', '1');

-- --------------------------------------------------------

--
-- Table structure for table `score`
--

CREATE TABLE `score` (
  `id` int(11) NOT NULL,
  `stage1` int(11) DEFAULT NULL,
  `stage2` int(11) DEFAULT NULL,
  `stage3` int(11) DEFAULT NULL,
  `stage4` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `score`
--

INSERT INTO `score` (`id`, `stage1`, `stage2`, `stage3`, `stage4`) VALUES
(2, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `stage`
--

CREATE TABLE `stage` (
  `id` int(11) NOT NULL,
  `stage_name` varchar(255) DEFAULT NULL,
  `q1` text DEFAULT NULL,
  `q2` text DEFAULT NULL,
  `q3` text DEFAULT NULL,
  `q4` text DEFAULT NULL,
  `q5` text DEFAULT NULL,
  `q6` text DEFAULT NULL,
  `q7` text DEFAULT NULL,
  `q8` text DEFAULT NULL,
  `q9` text DEFAULT NULL,
  `q10` text DEFAULT NULL,
  `a1` text DEFAULT NULL,
  `a2` text DEFAULT NULL,
  `a3` text DEFAULT NULL,
  `a4` text DEFAULT NULL,
  `a5` text DEFAULT NULL,
  `a6` text DEFAULT NULL,
  `a7` text DEFAULT NULL,
  `a8` text DEFAULT NULL,
  `a9` text DEFAULT NULL,
  `a10` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `stage`
--

INSERT INTO `stage` (`id`, `stage_name`, `q1`, `q2`, `q3`, `q4`, `q5`, `q6`, `q7`, `q8`, `q9`, `q10`, `a1`, `a2`, `a3`, `a4`, `a5`, `a6`, `a7`, `a8`, `a9`, `a10`) VALUES
(2, 'stage1', '3 + 4 = ?', '9 - 5 = ?', '2 * 6 = ?', '8 / 2 = ?', '5 + 7 = ?', '6 - 3 = ?', '3 * 5 = ?', '9 / 3 = ?', '7 + 2 = ?', '4 * 2 = ?', '7', '4', '12', '4', '12', '3', '15', '3', '9', '8'),
(3, 'stage2', 'hi how are you', '', '', '', '', '', '', '', '', '', 'i am fine', '', '', '', '', '', '', '', '', '');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `player`
--
ALTER TABLE `player`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `score`
--
ALTER TABLE `score`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `stage`
--
ALTER TABLE `stage`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `player`
--
ALTER TABLE `player`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `stage`
--
ALTER TABLE `stage`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `score`
--
ALTER TABLE `score`
  ADD CONSTRAINT `score_ibfk_1` FOREIGN KEY (`id`) REFERENCES `player` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
