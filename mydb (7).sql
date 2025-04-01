-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 01, 2025 at 11:50 AM
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
-- Database: `mydb`
--

-- --------------------------------------------------------

--
-- Table structure for table `attendance_history`
--

CREATE TABLE `attendance_history` (
  `id` int(11) NOT NULL,
  `student_id` varchar(20) NOT NULL,
  `classroom_id` int(11) NOT NULL,
  `date_time` datetime DEFAULT NULL,
  `status` enum('มาตรงเวลา','มาสาย','ขาดเรียน','ลากิจ','ลาป่วย') NOT NULL,
  `total_attendance` int(11) DEFAULT 0,
  `day` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `attendance_history`
--

INSERT INTO `attendance_history` (`id`, `student_id`, `classroom_id`, `date_time`, `status`, `total_attendance`, `day`) VALUES
(109, '6421604803', 56, '2024-11-01 01:12:38', 'มาสาย', 1, 1),
(112, '6421604803', 56, '2024-11-05 01:26:08', 'มาสาย', 2, 2),
(113, '6421604803', 56, '2024-11-10 01:26:56', 'มาสาย', 3, 3),
(132, '6421604803', 56, '2024-11-10 15:39:54', 'มาตรงเวลา', 4, 4),
(133, '6421604803', 56, '2024-11-11 19:50:06', 'ขาดเรียน', 5, 5),
(134, '6421604803', 56, '2024-11-11 19:50:50', 'มาตรงเวลา', 6, 6),
(135, '6421604803', 56, '2024-11-11 20:47:57', 'มาสาย', 8, 7),
(136, '6421604803', 56, '2024-11-11 20:48:30', 'มาสาย', 9, 8),
(137, '6421604803', 56, '2024-11-11 20:48:30', 'มาสาย', 12, 9),
(138, '6421604803', 56, '2024-11-11 20:49:04', 'มาสาย', 7, 10),
(139, '6421604803', 56, '2024-11-11 20:49:04', 'มาสาย', 10, 11),
(140, '6421604803', 56, '2024-11-11 20:49:38', 'มาสาย', 11, 12),
(141, '6421604803', 56, '2024-11-11 20:49:38', 'มาสาย', 13, 13),
(142, '6421604803', 56, '2024-11-11 20:50:12', 'ขาดเรียน', 14, 14),
(143, '6421604803', 56, '2024-11-11 20:50:12', 'ขาดเรียน', 15, 15),
(167, '6421604804', 56, NULL, 'ขาดเรียน', 0, 1),
(168, '6421604804', 56, NULL, 'ขาดเรียน', 0, 2),
(169, '6421604804', 56, NULL, 'ขาดเรียน', 0, 3);

-- --------------------------------------------------------

--
-- Table structure for table `classrooms`
--

CREATE TABLE `classrooms` (
  `id` int(11) NOT NULL,
  `code` varchar(8) NOT NULL,
  `teacher_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `days` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`days`)),
  `endTime` time DEFAULT NULL,
  `group` varchar(255) DEFAULT NULL,
  `room` varchar(255) DEFAULT NULL,
  `startTime` time DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `subject` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `classrooms`
--

INSERT INTO `classrooms` (`id`, `code`, `teacher_id`, `created_at`, `days`, `endTime`, `group`, `room`, `startTime`, `type`, `subject`) VALUES
(19, 'Z94Df3sX', 4, '2024-10-05 07:38:45', '[\"Monday\",\"Friday\"]', '15:38:00', '7001', 'sc-9325', '15:38:00', 'Lab', 'Math1'),
(20, 'oJeLbkyT', 4, '2024-10-05 08:35:18', '[\"Tuesday\",\"Sunday\",\"Monday\"]', '03:35:00', '700', 'LH-4 330', '15:35:00', 'Lab', 'JojaCola'),
(21, 'QerRbDXg', 4, '2024-10-05 08:39:14', '[\"W\",\"M\"]', '16:39:00', '710', 'sc-9325', '16:39:00', 'Lecture', 'Math123'),
(25, 'cJ7Oxgul', 4, '2024-10-09 02:31:31', '[\"Tuesday\",\"Sunday\",\"Wednesday\"]', '17:31:00', '710', 'sc-9-3301', '14:31:00', 'Lecture', 'javaedittest'),
(26, 'S1hh7WNk', 4, '2024-10-09 15:29:23', '[\"Monday\",\"Friday\"]', '00:28:00', '700', 'sc-9-33011111', '11:28:00', 'Lab', 'py'),
(28, 'yr8uyKeQ', 4, '2024-10-13 01:12:16', '[\"Tuesday\",\"Wednesday\"]', '10:12:00', '700', 'sc-9-330', '09:12:00', 'Lecture', 'pyหฟกฟ'),
(51, 'pRHwO0WI', 4, '2024-10-21 13:03:59', '[\"Tuesday\",\"Wednesday\"]', '23:03:00', '700wasda', 'sc-9-3301', '23:05:00', 'Lab', '๋Joja1'),
(53, 'tDzB5meG', 1, '2024-10-23 13:48:13', '[\"Wednesday\",\"Tuesday\"]', '12:52:00', '700wasda', 'sc-9-330///', '23:48:00', 'Lecture', 'as'),
(56, 'u9byfSRn', 4, '2024-10-27 00:32:05', '[\"Tuesday\",\"Wednesday\"]', '08:00:00', '700wasd', 'sc-9-330ssss', '07:50:00', 'Lecture', 'GGEZ'),
(57, 'Ysam2Kak', 5, '2024-11-04 16:24:10', '[\"Tuesday\",\"Wednesday\"]', '12:24:00', '700wasda', 'sc-9330', '12:24:00', 'Lecture', 'Math'),
(58, 'iOGB7lrB', 4, '2024-11-05 15:25:26', '[\"Wednesday\",\"Tuesday\"]', '22:30:00', '700wasda', 'sc-9330', '13:29:00', 'Lecture', 'Math'),
(61, 'tEJFFZ7x', 4, '2024-11-07 06:28:37', '[\"Thursday\",\"Wednesday\",\"Tuesday\"]', '17:28:00', '700wasda', 'sc-9330', '16:28:00', 'Lecture', 'Math');

-- --------------------------------------------------------

--
-- Table structure for table `classroom_members`
--

CREATE TABLE `classroom_members` (
  `id` int(11) NOT NULL,
  `classroom_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `joined_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `classroom_members`
--

INSERT INTO `classroom_members` (`id`, `classroom_id`, `student_id`, `joined_at`) VALUES
(1, 25, 1, '2024-10-08 14:01:56'),
(4, 26, 1, '2024-10-09 15:42:49'),
(10, 20, 9, '2024-10-16 23:14:36'),
(14, 28, 1, '2024-10-17 03:02:04'),
(64, 51, 4, '2024-10-26 05:13:39'),
(69, 56, 1, '2024-10-27 00:33:23'),
(77, 21, 4, '2024-11-07 03:56:29'),
(78, 21, 9, '2024-11-07 03:57:50'),
(97, 21, 1, '2024-11-07 06:51:00'),
(116, 56, 13, '2024-11-07 22:21:39'),
(117, 21, 17, '2024-11-08 04:24:15');

-- --------------------------------------------------------

--
-- Table structure for table `keytap`
--

CREATE TABLE `keytap` (
  `id` int(11) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `keytap`
--

INSERT INTO `keytap` (`id`, `password`) VALUES
(1, '$2b$10$ZyqJAvUhxgOXTOaDQ2NLtu8t2MpYFSLIO9dvKQfhVbdGGvDJ0BfpW');

-- --------------------------------------------------------

--
-- Table structure for table `nisit`
--

CREATE TABLE `nisit` (
  `id` int(11) NOT NULL,
  `studentId` varchar(20) NOT NULL,
  `fname` varchar(50) NOT NULL,
  `lname` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `major` varchar(50) DEFAULT NULL,
  `faculty` varchar(50) DEFAULT NULL,
  `role` enum('nisit') DEFAULT 'nisit',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `nisit`
--

INSERT INTO `nisit` (`id`, `studentId`, `fname`, `lname`, `email`, `password`, `major`, `faculty`, `role`, `created_at`, `updated_at`) VALUES
(1, '6421604803', 'ณัฐณภัทร', 'เพ็ชเรือง', 'natnapat262@gmail.com', '$2b$10$0Qc2abOt9zTySeEFP/0lP.pLzljcwcfXw8eAs2disSaauovo2BiVy', '๋Joja', 'asdas', 'nisit', '2024-09-23 03:07:12', '2024-11-06 08:11:48'),
(3, '6421604808', 'ณัฐณภัทร', 'เพ็ชเรือง', 'natnapat1@ku.th', '$2b$10$D.6Yb5yWtjhD5CAhqUwwo.sXD5BhZht7nOZvT1h.e5r219/wcFuiu', 'sadasd', 'asdas', 'nisit', '2024-09-23 08:17:41', '2024-09-25 12:14:14'),
(4, '6421604827', 'ณัฐณภัทร', 'เพ็ชเรือง', 'natnapat2@ku.th', '$2b$10$WPilChUkEhshkKC1Bc/gg.RI1wXbl/25wwzQ1KRGIHZNCHk95fMxK', 'sadasd', 'asdas', 'nisit', '2024-09-25 10:18:29', '2024-11-09 09:12:41'),
(5, '6421604801', 'ณัฐณภัทร', 'เพ็ชเรือง', 'natnapat3@ku.th', '$2b$10$D3HCelqclk.lM7AQtUSu4.UVxmAHUwCycM05c2rd0lojKXnCaQuN6', 'sadasd', 'asdas', 'nisit', '2024-09-25 10:32:32', '2024-09-25 12:14:24'),
(9, '6421604877', 'ณัฐณภัทร', 'เพ็ชเรือง', 'natnapat4@ku.th', '$2b$10$/LjkFvc5ilfLiead3Nk.BeHCkH2zPTfEDy3cMK68mQUFZIvNjFxQS', 'sadasd', 'asdas', 'nisit', '2024-09-25 12:14:49', '2024-09-25 12:14:49'),
(10, '6421604871', 'ณัฐณภัทร', 'เพ็ชเรือง', 'natnapat5@ku.th', '$2b$10$kdI4UxmHR9bztTriWI/xtOaAnot3..HLHdCan2ICYAbt7Y6N0wzgS', 'sadasd', 'asdas', 'nisit', '2024-09-25 12:15:45', '2024-09-25 12:15:45'),
(13, '6421604804', 'ณัฐณภัทร', 'เพ็ชเรือง', 'natnapat9@ku.th', '$2b$10$KwOrqVNJvJw3MT1QrKnL/.7NuxcNOu0tsXeoLUW5A6rq.kYXI6UCO', 'sadasdaaa', 'asdas', 'nisit', '2024-11-07 09:17:02', '2024-11-07 21:51:44'),
(17, '6421604809', 'Natnaphat', 'Phetrueang', 'natnapat8@ku.th', '$2b$10$pkgiqcIzmDitDwTEag9dteFEezziFiKm3cOqY9ddbQeHvEwMJByTO', 'comsci', 'aaa', 'nisit', '2024-11-08 04:08:25', '2024-11-08 04:19:04'),
(31, '64216048077', 'ณัฐณภัทร', 'เพ็ชเรือง', 'natnapat262@ku.th', '$2b$10$JqIIk9QnxqqJvFV69Q46ceNZo5pL9LZDJbJvLqEkcC/vW5e4LcSQe', 'comsci', 'aa', 'nisit', '2024-11-10 07:44:39', '2024-11-10 07:44:39'),
(32, '6421604811', 'ณัฐณภัทร', 'เพ็ชเรือง', 'natnapat642@ku.th', '$2b$10$JMdUB76rW7V.JA.yITc.bOEDjofzqfWc3EHs19d.a8mDmgJlPi13.', 'comsci', 'aa', 'nisit', '2024-11-10 07:50:01', '2024-11-10 07:50:01'),
(33, '6421604888', 'Natnaphat', 'Phetrueang', 'natnapat20@ku.th', '$2b$10$5e5/InJFeGKedhoowelRj.Md0WW3d9eIx63zKpubIhbfLwVaw0W46', 'comsci', 'aa', 'nisit', '2024-11-10 08:35:59', '2024-11-10 08:35:59');

-- --------------------------------------------------------

--
-- Table structure for table `reset_tokens`
--

CREATE TABLE `reset_tokens` (
  `id` int(11) NOT NULL,
  `token` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `expires_at` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reset_tokens`
--

INSERT INTO `reset_tokens` (`id`, `token`, `created_at`, `expires_at`, `user_id`) VALUES
(14, '40a27f357a26e831cc888d86643facbbcc68b420081e499f1395739d0313ca9e', '2024-11-03 14:04:06', '2024-11-04 14:04:06', 1),
(15, '08ec71e7659b7c51efa3c8e2efead8de37c2f88490899fce158880113f3b43f5', '2024-11-04 16:01:35', '2024-11-05 16:01:35', 5),
(16, '83eecb00d140a1e305390b3c9017f5f06bf9b1f7af35fcb68447fd6cba4a9360', '2024-11-04 16:02:36', '2024-11-05 16:02:36', 1);

-- --------------------------------------------------------

--
-- Table structure for table `teacher`
--

CREATE TABLE `teacher` (
  `id` int(11) NOT NULL,
  `fname` varchar(50) NOT NULL,
  `lname` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('teacher') DEFAULT 'teacher',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `teacher`
--

INSERT INTO `teacher` (`id`, `fname`, `lname`, `email`, `password`, `role`, `created_at`, `updated_at`) VALUES
(1, 'ณัฐณภัทรsaaad', 'เพ็ชเรือง', 'natnaphat.p@ku.th', '$2b$10$KPXMnE2VjzC/3exyVpe9uuAU3bAgiCzypkZ9szfMb091ywDZ.j7hC', 'teacher', '2024-09-23 03:07:45', '2024-10-22 06:54:55'),
(2, 'ณัฐณภัทร', 'เพ็ชเรือง', 'natnaphat1@ku.th', '$2b$10$jWZTM8asbKqcB8cV5HqNHOWgpqi5fh5vl/C5qmepfL7bmf0N8ZQYa', 'teacher', '2024-09-23 08:18:11', '2024-09-23 08:18:11'),
(3, 'ณัฐณภัทร', 'เพ็ชเรือง', 'natnaphat2@ku.th', '$2b$10$uc2fubheW9DXOUtEyEI.5efUQXywx5IlH8xe.DBcufBPbZECoz1Cy', 'teacher', '2024-09-24 15:53:42', '2024-09-24 15:53:42'),
(4, 'Natnaphat', 'Phetrueang', 'natnaphat3@ku.th', '$2b$10$cJca6xvo/X6NbxLXDW6StOBsdOp4aK1vmJeoY1azT61SN2jeyicue', 'teacher', '2024-10-03 02:24:57', '2024-11-10 08:05:52'),
(5, 'ณัฐณภัทร', 'เพ็ชเรือง', 'natnaphat@ku.th', '$2b$10$03nsz/mspEVGeHLjaVURnecj7KCWfRtHyjZAD1AUj6E4TnNHKyfj2', 'teacher', '2024-11-04 15:37:52', '2024-11-04 15:37:52'),
(6, 'a', 'b', 'natnaphat6@ku.th', '$2b$10$6i629/jWInyLSS5K2NtU1OAIq669k87Ugk0IXSsqqPI0XzshgJPai', 'teacher', '2024-11-05 08:09:55', '2024-11-05 08:09:55');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `attendance_history`
--
ALTER TABLE `attendance_history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `student_id` (`student_id`),
  ADD KEY `classroom_id` (`classroom_id`);

--
-- Indexes for table `classrooms`
--
ALTER TABLE `classrooms`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`),
  ADD KEY `teacher_id` (`teacher_id`);

--
-- Indexes for table `classroom_members`
--
ALTER TABLE `classroom_members`
  ADD PRIMARY KEY (`id`),
  ADD KEY `classroom_id` (`classroom_id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indexes for table `keytap`
--
ALTER TABLE `keytap`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `nisit`
--
ALTER TABLE `nisit`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `studentId` (`studentId`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `reset_tokens`
--
ALTER TABLE `reset_tokens`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `teacher`
--
ALTER TABLE `teacher`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `attendance_history`
--
ALTER TABLE `attendance_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=170;

--
-- AUTO_INCREMENT for table `classrooms`
--
ALTER TABLE `classrooms`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=65;

--
-- AUTO_INCREMENT for table `classroom_members`
--
ALTER TABLE `classroom_members`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=118;

--
-- AUTO_INCREMENT for table `keytap`
--
ALTER TABLE `keytap`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `nisit`
--
ALTER TABLE `nisit`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `reset_tokens`
--
ALTER TABLE `reset_tokens`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `teacher`
--
ALTER TABLE `teacher`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `attendance_history`
--
ALTER TABLE `attendance_history`
  ADD CONSTRAINT `attendance_history_ibfk_2` FOREIGN KEY (`classroom_id`) REFERENCES `classrooms` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `classrooms`
--
ALTER TABLE `classrooms`
  ADD CONSTRAINT `classrooms_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `classroom_members`
--
ALTER TABLE `classroom_members`
  ADD CONSTRAINT `classroom_members_ibfk_1` FOREIGN KEY (`classroom_id`) REFERENCES `classrooms` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `classroom_members_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `nisit` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
