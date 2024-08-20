-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 20, 2024 at 05:28 PM
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
  `Stage3` int(11) DEFAULT NULL,
  `stage4` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `score`
--

INSERT INTO `score` (`id`, `stage1`, `stage2`, `Stage3`, `stage4`) VALUES
(2, 2507, 155, 12, NULL);

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
(2, 'stage1', 'Find the next four terms of the arithmetic sequence 16, 24, 32, ...', 'Determine the 10th term of the sequence -17, -13, -9, ...', 'Write an equation for the nth term of the arithmetic sequence 18, 30, 42, 54, 66', 'Determine the sum of an arithmetic series where n = 45, a = 14.3, and Tn = 80.3', 'What is Sn if a = 27.5, d = 1.5 and n = 35?', 'Find the first three terms of the arithmetic series in which a = 6, Tn = 201, and Sn = 4140', 'Find the next two terms of the geometric sequence 64, -32, 16, -8, ...', 'Write the first four terms of the geometric sequence in which a1=-3 and r = -4', 'What is the fifth term of a geometric sequence if T1= 7 and r = 0.2?', 'Find the sum of the first five terms of the geometric series for which a =2 and r = 2', '40, 48, 56, 64', '19', '12n + 6', '2128.5', '1855', '6, 11, 16', '4, -2', '-3, 12, -48, 192', '0.0112', '62'),
(3, 'stage2', 'A function f is given by f(x) = x2 - x + 1. Find f(2)', 'Given that f(x) = x^3 + 2x^2 and g(x) = 3x^2 - 1. Find (f + g)(x)', 'Given that f(x) = x^3 + 2x^2 and g(x) = 3x^2 - 1. Find (fg)(x)', 'Given that f(x) = x^3 + 2x^2 and g(x) = 3x^2 - 1. Find 3f(x) + g(x) + 5', 'Given f(x) = 5x - 1 and g(x) = 4x. Find (g o f)(x)', 'Given f(x) = 5x - 1 and g(x) = 4x. Find (f o g)(x) ', 'Given f(x) = 2x^2 + x and g(x) = x + 3. Find (g o f)(x)', 'Given f(x) = 2x^2 + x and g(x)= x + 3. Find (f o g)(x)', 'Find the inverse of the function (if it exists) given by f(x) = x^2 - 1', 'Given that f(x) is a linear function such that f(2) = 5 and f(4) = 8, find f(x)', 'f(2) = 3', 'f + g = x^3 + 5x^2 - 1', '3x^5 - x^3 + 6x^4 - 2x', '3x^3 + 9x^2 + 4', '20x - 4', '20x - 1', '2x^2 + x + 3', '2x^2 + 13x + 21', 'y = x^2 - 1 is not a one-to-one function, thus F has no inverse', '2 + 1.5x'),
(6, 'Stage3', 'Factorize x^2 + 7x - 55 = - 25', 'Factorize - 7x^2 - 34 = -11x^2 - 11x + 11', 'Factorize x^2 + 10x - 9 = 2x^2', 'Factorize 7x^2 - 10x + 6 = 2x^2 + x', 'Use the quadratic formula to solve - 7x^2 - 4x + 3 = 0', 'Use the quadratic formula to solve 32x^2 + 64 = 24x^2 - 72x', 'Solve x^2 + 10x - 4 = 0 by completing the square.', 'Solve x^2 - 20x + 36 = 0 by completing the square', 'Solve 12 + 6x - x^2 = 0 by completing the square', 'Find the nature of the roots of x (2x - 1) = 10', '-10, 3', '9/4, -5', '1, 9', '6/5, 1', '3/7, -1, there are two real solutions', '-1, -8, there are two real solutions', '0.4, -10.4', '18, 2', '7.6, -1.6', 'There are two real solutions'),
(7, 'stage4', 'Express in logarithmic form for 7^3 = 343', 'Express in logarithmic form for 4^5 = 1024', 'Express in logarithmic form for 8^2 = 64', 'Express in exponential form for log7 49 = 2', 'Express in exponential form for log8 64 = 2', 'Calculate 2log2 12 + 3log2 5 - log2 15 - log2 150', 'Determine the value of log7 2401', 'Determine the value of log9 729', 'Solve unknown logh 4096 = 6', 'Solve unknown log16 16 = n', 'log7 343 = 3', 'log4 1024 = 5', 'log8 64 = 2', '7^2 = 49', '8^2 = 64', '3', '4', '3', '4', '1');

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

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
