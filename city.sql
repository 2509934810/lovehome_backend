-- --------------------------------------------------------
-- 主机:                           127.0.0.1
-- 服务器版本:                        10.5.2-MariaDB - mariadb.org binary distribution
-- 服务器OS:                        Win64
-- HeidiSQL 版本:                  10.2.0.5599
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


DELETE FROM `user_addr`;
INSERT INTO `user_addr` (`id`, `province`, `city`, `code`) VALUES
	(1, '北京市', '北京市', 110100),
	(2, '天津市', '天津市', 120100),
	(3, '河北省', '石家庄市', 130100),
	(4, '河北省', '唐山市', 130200),
	(5, '河北省', '秦皇岛市', 130300),
	(6, '河北省', '邯郸市', 130400),
	(7, '河北省', '邢台市', 130500),
	(8, '河北省', '保定市', 130600),
	(9, '河北省', '张家口市', 130700),
	(10, '河北省', '承德市', 130800),
	(11, '河北省', '沧州市', 130900),
	(12, '河北省', '廊坊市', 131000),
	(13, '河北省', '衡水市', 131100),
	(14, '山西省', '太原市', 140100),
	(15, '山西省', '大同市', 140200),
	(16, '山西省', '阳泉市', 140300),
	(17, '山西省', '长治市', 140400),
	(18, '山西省', '晋城市', 140500),
	(19, '山西省', '朔州市', 140600),
	(20, '山西省', '晋中市', 140700),
	(21, '山西省', '运城市', 140800),
	(22, '山西省', '忻州市', 140900),
	(23, '山西省', '临汾市', 141000),
	(24, '山西省', '吕梁市', 141100),
	(25, '内蒙古自治区', '呼和浩特市', 150100),
	(26, '内蒙古自治区', '包头市', 150200),
	(27, '内蒙古自治区', '乌海市', 150300),
	(28, '内蒙古自治区', '赤峰市', 150400),
	(29, '内蒙古自治区', '通辽市', 150500),
	(30, '内蒙古自治区', '鄂尔多斯市', 150600),
	(31, '内蒙古自治区', '呼伦贝尔市', 150700),
	(32, '内蒙古自治区', '巴彦淖尔市', 150800),
	(33, '内蒙古自治区', '乌兰察布市', 150900),
	(34, '内蒙古自治区', '兴安盟', 152200),
	(35, '内蒙古自治区', '锡林郭勒盟', 152500),
	(36, '内蒙古自治区', '二连浩特市', 152501),
	(37, '内蒙古自治区', '锡林浩特市', 152502),
	(38, '内蒙古自治区', '阿拉善盟', 152900),
	(39, '辽宁省', '沈阳市', 210100),
	(40, '辽宁省', '大连市', 210200),
	(41, '辽宁省', '鞍山市', 210300),
	(42, '辽宁省', '抚顺市', 210400),
	(43, '辽宁省', '本溪市', 210500),
	(44, '辽宁省', '丹东市', 210600),
	(45, '辽宁省', '锦州市', 210700),
	(46, '辽宁省', '营口市', 210800),
	(47, '辽宁省', '阜新市', 210900),
	(48, '辽宁省', '辽阳市', 211000),
	(49, '辽宁省', '盘锦市', 211100),
	(50, '辽宁省', '铁岭市', 211200),
	(51, '辽宁省', '朝阳市', 211300),
	(52, '辽宁省', '葫芦岛市', 211400),
	(53, '吉林省', '长春市', 220100),
	(54, '吉林省', '吉林市', 220200),
	(55, '吉林省', '四平市', 220300),
	(56, '吉林省', '辽源市', 220400),
	(57, '吉林省', '通化市', 220500),
	(58, '吉林省', '白山市', 220600),
	(59, '吉林省', '松原市', 220700),
	(60, '吉林省', '白城市', 220800),
	(61, '吉林省', '延边朝鲜族自治州', 222400),
	(62, '黑龙江省', '哈尔滨市', 230100),
	(63, '黑龙江省', '齐齐哈尔市', 230200),
	(64, '黑龙江省', '鸡西市', 230300),
	(65, '黑龙江省', '鹤岗市', 230400),
	(66, '黑龙江省', '双鸭山市', 230500),
	(67, '黑龙江省', '大庆市', 230600),
	(68, '黑龙江省', '伊春市', 230700),
	(69, '黑龙江省', '佳木斯市', 230800),
	(70, '黑龙江省', '七台河市', 230900),
	(71, '黑龙江省', '牡丹江市', 231000),
	(72, '黑龙江省', '黑河市', 231100),
	(73, '黑龙江省', '绥化市', 231200),
	(74, '黑龙江省', '大兴安岭地区', 232700),
	(75, '上海市', '上海市', 310100),
	(76, '江苏省', '南京市', 320100),
	(77, '江苏省', '无锡市', 320200),
	(78, '江苏省', '徐州市', 320300),
	(79, '江苏省', '常州市', 320400),
	(80, '江苏省', '苏州市', 320500),
	(81, '江苏省', '昆山市', 320583),
	(82, '江苏省', '南通市', 320600),
	(83, '江苏省', '连云港市', 320700),
	(84, '江苏省', '淮安市', 320800),
	(85, '江苏省', '盐城市', 320900),
	(86, '江苏省', '扬州市', 321000),
	(87, '江苏省', '镇江市', 321100),
	(88, '江苏省', '泰州市', 321200),
	(89, '江苏省', '宿迁市', 321300),
	(90, '浙江省', '杭州市', 330100),
	(91, '浙江省', '宁波市', 330200),
	(92, '浙江省', '温州市', 330300),
	(93, '浙江省', '嘉兴市', 330400),
	(94, '浙江省', '湖州市', 330500),
	(95, '浙江省', '绍兴市', 330600),
	(96, '浙江省', '金华市', 330700),
	(97, '浙江省', '衢州市', 330800),
	(98, '浙江省', '舟山市', 330900),
	(99, '浙江省', '台州市', 331000),
	(100, '浙江省', '丽水市', 331100),
	(101, '安徽省', '合肥市', 340100),
	(102, '安徽省', '芜湖市', 340200),
	(103, '安徽省', '蚌埠市', 340300),
	(104, '安徽省', '淮南市', 340400),
	(105, '安徽省', '马鞍山市', 340500),
	(106, '安徽省', '淮北市', 340600),
	(107, '安徽省', '铜陵市', 340700),
	(108, '安徽省', '安庆市', 340800),
	(109, '安徽省', '黄山市', 341000),
	(110, '安徽省', '滁州市', 341100),
	(111, '安徽省', '阜阳市', 341200),
	(112, '安徽省', '宿州市', 341300),
	(113, '安徽省', '六安市', 341500),
	(114, '安徽省', '亳州市', 341600),
	(115, '安徽省', '池州市', 341700),
	(116, '安徽省', '宣城市', 341800),
	(117, '福建省', '福州市', 350100),
	(118, '福建省', '厦门市', 350200),
	(119, '福建省', '莆田市', 350300),
	(120, '福建省', '三明市', 350400),
	(121, '福建省', '泉州市', 350500),
	(122, '福建省', '漳州市', 350600),
	(123, '福建省', '南平市', 350700),
	(124, '福建省', '龙岩市', 350800),
	(125, '福建省', '宁德市', 350900),
	(126, '江西省', '南昌市', 360100),
	(127, '江西省', '景德镇市', 360200),
	(128, '江西省', '萍乡市', 360300),
	(129, '江西省', '九江市', 360400),
	(130, '江西省', '新余市', 360500),
	(131, '江西省', '鹰潭市', 360600),
	(132, '江西省', '赣州市', 360700),
	(133, '江西省', '吉安市', 360800),
	(134, '江西省', '宜春市', 360900),
	(135, '江西省', '抚州市', 361000),
	(136, '江西省', '上饶市', 361100),
	(137, '山东省', '济南市', 370100),
	(138, '山东省', '青岛市', 370200),
	(139, '山东省', '淄博市', 370300),
	(140, '山东省', '枣庄市', 370400),
	(141, '山东省', '滕州市', 370481),
	(142, '山东省', '东营市', 370500),
	(143, '山东省', '烟台市', 370600),
	(144, '山东省', '潍坊市', 370700),
	(145, '山东省', '济宁市', 370800),
	(146, '山东省', '泰安市', 370900),
	(147, '山东省', '威海市', 371000),
	(148, '山东省', '日照市', 371100),
	(149, '山东省', '莱芜市', 371200),
	(150, '山东省', '临沂市', 371300),
	(151, '山东省', '德州市', 371400),
	(152, '山东省', '聊城市', 371500),
	(153, '山东省', '滨州市', 371600),
	(154, '山东省', '菏泽市', 371700),
	(155, '河南省', '郑州市', 410100),
	(156, '河南省', '开封市', 410200),
	(157, '河南省', '洛阳市', 410300),
	(158, '河南省', '平顶山市', 410400),
	(159, '河南省', '安阳市', 410500),
	(160, '河南省', '鹤壁市', 410600),
	(161, '河南省', '新乡市', 410700),
	(162, '河南省', '焦作市', 410800),
	(163, '河南省', '濮阳市', 410900),
	(164, '河南省', '许昌市', 411000),
	(165, '河南省', '漯河市', 411100),
	(166, '河南省', '三门峡市', 411200),
	(167, '河南省', '南阳市', 411300),
	(168, '河南省', '商丘市', 411400),
	(169, '河南省', '信阳市', 411500),
	(170, '河南省', '周口市', 411600),
	(171, '河南省', '驻马店市', 411700),
	(172, '河南省', '济源市', 419001),
	(173, '湖北省', '武汉市', 420100),
	(174, '湖北省', '黄石市', 420200),
	(175, '湖北省', '十堰市', 420300),
	(176, '湖北省', '宜昌市', 420500),
	(177, '湖北省', '襄阳市', 420600),
	(178, '湖北省', '鄂州市', 420700),
	(179, '湖北省', '荆门市', 420800),
	(180, '湖北省', '孝感市', 420900),
	(181, '湖北省', '荆州市', 421000),
	(182, '湖北省', '黄冈市', 421100),
	(183, '湖北省', '咸宁市', 421200),
	(184, '湖北省', '随州市', 421300),
	(185, '湖北省', '恩施土家族苗族自治州', 422800),
	(186, '湖北省', '潜江市', 429005),
	(187, '湖南省', '长沙市', 430100),
	(188, '湖南省', '株洲市', 430200),
	(189, '湖南省', '湘潭市', 430300),
	(190, '湖南省', '衡阳市', 430400),
	(191, '湖南省', '邵阳市', 430500),
	(192, '湖南省', '岳阳市', 430600),
	(193, '湖南省', '常德市', 430700),
	(194, '湖南省', '张家界市', 430800),
	(195, '湖南省', '益阳市', 430900),
	(196, '湖南省', '郴州市', 431000),
	(197, '湖南省', '永州市', 431100),
	(198, '湖南省', '怀化市', 431200),
	(199, '湖南省', '娄底市', 431300),
	(200, '湖南省', '湘西土家族苗族自治州', 433100),
	(201, '广东省', '广州市', 440100),
	(202, '广东省', '韶关市', 440200),
	(203, '广东省', '深圳市', 440300),
	(204, '广东省', '珠海市', 440400),
	(205, '广东省', '汕头市', 440500),
	(206, '广东省', '佛山市', 440600),
	(207, '广东省', '江门市', 440700),
	(208, '广东省', '湛江市', 440800),
	(209, '广东省', '茂名市', 440900),
	(210, '广东省', '肇庆市', 441200),
	(211, '广东省', '惠州市', 441300),
	(212, '广东省', '梅州市', 441400),
	(213, '广东省', '汕尾市', 441500),
	(214, '广东省', '河源市', 441600),
	(215, '广东省', '阳江市', 441700),
	(216, '广东省', '清远市', 441800),
	(217, '广东省', '东莞市', 441900),
	(218, '广东省', '中山市', 442000),
	(219, '广东省', '潮州市', 445100),
	(220, '广东省', '揭阳市', 445200),
	(221, '广东省', '云浮市', 445300),
	(222, '广西壮族自治区', '南宁市', 450100),
	(223, '广西壮族自治区', '柳州市', 450200),
	(224, '广西壮族自治区', '桂林市', 450300),
	(225, '广西壮族自治区', '梧州市', 450400),
	(226, '广西壮族自治区', '北海市', 450500),
	(227, '广西壮族自治区', '防城港市', 450600),
	(228, '广西壮族自治区', '钦州市', 450700),
	(229, '广西壮族自治区', '贵港市', 450800),
	(230, '广西壮族自治区', '玉林市', 450900),
	(231, '广西壮族自治区', '百色市', 451000),
	(232, '广西壮族自治区', '贺州市', 451100),
	(233, '广西壮族自治区', '河池市', 451200),
	(234, '广西壮族自治区', '来宾市', 451300),
	(235, '广西壮族自治区', '崇左市', 451400),
	(236, '海南省', '海口市', 460100),
	(237, '海南省', '三亚市', 460200),
	(238, '海南省', '儋州市', 460400),
	(239, '重庆市', '重庆市', 500100),
	(240, '四川省', '成都市', 510100),
	(241, '四川省', '自贡市', 510300),
	(242, '四川省', '攀枝花市', 510400),
	(243, '四川省', '泸州市', 510500),
	(244, '四川省', '德阳市', 510600),
	(245, '四川省', '绵阳市', 510700),
	(246, '四川省', '广元市', 510800),
	(247, '四川省', '遂宁市', 510900),
	(248, '四川省', '内江市', 511000),
	(249, '四川省', '乐山市', 511100),
	(250, '四川省', '南充市', 511300),
	(251, '四川省', '眉山市', 511400),
	(252, '四川省', '宜宾市', 511500),
	(253, '四川省', '广安市', 511600),
	(254, '四川省', '达州市', 511700),
	(255, '四川省', '雅安市', 511800),
	(256, '四川省', '巴中市', 511900),
	(257, '四川省', '资阳市', 512000),
	(258, '四川省', '阿坝藏族羌族自治州', 513200),
	(259, '四川省', '甘孜藏族自治州', 513300),
	(260, '四川省', '凉山彝族自治州', 513400),
	(261, '贵州省', '贵阳市', 520100),
	(262, '贵州省', '六盘水市', 520200),
	(263, '贵州省', '遵义市', 520300),
	(264, '贵州省', '安顺市', 520400),
	(265, '贵州省', '毕节市', 520500),
	(266, '贵州省', '铜仁市', 520600),
	(267, '贵州省', '黔西南布依族苗族自治州', 522300),
	(268, '贵州省', '黔东南苗族侗族自治州', 522600),
	(269, '贵州省', '黔南布依族苗族自治州', 522700),
	(270, '云南省', '昆明市', 530100),
	(271, '云南省', '曲靖市', 530300),
	(272, '云南省', '玉溪市', 530400),
	(273, '云南省', '保山市', 530500),
	(274, '云南省', '昭通市', 530600),
	(275, '云南省', '丽江市', 530700),
	(276, '云南省', '普洱市', 530800),
	(277, '云南省', '临沧市', 530900),
	(278, '云南省', '楚雄彝族自治州', 532300),
	(279, '云南省', '红河哈尼族彝族自治州', 532500),
	(280, '云南省', '文山壮族苗族自治州', 532600),
	(281, '云南省', '西双版纳傣族自治州', 532800),
	(282, '云南省', '大理白族自治州', 532900),
	(283, '云南省', '德宏傣族景颇族自治州', 533100),
	(284, '云南省', '怒江傈僳族自治州', 533300),
	(285, '云南省', '迪庆藏族自治州', 533400),
	(286, '西藏自治区', '拉萨市', 540100),
	(287, '西藏自治区', '日喀则市', 540200),
	(288, '陕西省', '西安市', 610100),
	(289, '陕西省', '铜川市', 610200),
	(290, '陕西省', '宝鸡市', 610300),
	(291, '陕西省', '咸阳市', 610400),
	(292, '陕西省', '渭南市', 610500),
	(293, '陕西省', '延安市', 610600),
	(294, '陕西省', '汉中市', 610700),
	(295, '陕西省', '榆林市', 610800),
	(296, '陕西省', '安康市', 610900),
	(297, '陕西省', '商洛市', 611000),
	(298, '甘肃省', '兰州市', 620100),
	(299, '甘肃省', '嘉峪关市', 620200),
	(300, '甘肃省', '金昌市', 620300),
	(301, '甘肃省', '白银市', 620400),
	(302, '甘肃省', '天水市', 620500),
	(303, '甘肃省', '武威市', 620600),
	(304, '甘肃省', '张掖市', 620700),
	(305, '甘肃省', '平凉市', 620800),
	(306, '甘肃省', '酒泉市', 620900),
	(307, '甘肃省', '庆阳市', 621000),
	(308, '甘肃省', '定西市', 621100),
	(309, '甘肃省', '陇南市', 621200),
	(310, '甘肃省', '临夏回族自治州', 622900),
	(311, '甘肃省', '甘南藏族自治州', 623000),
	(312, '青海省', '西宁市', 630100),
	(313, '青海省', '海东市', 630200),
	(314, '青海省', '海西蒙古族藏族自治州', 632800),
	(315, '宁夏回族自治区', '银川市', 640100),
	(316, '宁夏回族自治区', '石嘴山市', 640200),
	(317, '宁夏回族自治区', '吴忠市', 640300),
	(318, '新疆维吾尔自治区', '乌鲁木齐市', 650100),
	(319, '新疆维吾尔自治区', '克拉玛依市', 650200),
	(320, '新疆维吾尔自治区', '哈密市', 650500),
	(321, '新疆维吾尔自治区', '昌吉回族自治州', 652300),
	(322, '新疆维吾尔自治区', '巴音郭楞蒙古自治州', 652800),
	(323, '新疆维吾尔自治区', '阿克苏地区', 652900),
	(324, '新疆维吾尔自治区', '喀什地区', 653100),
	(325, '新疆维吾尔自治区', '伊犁哈萨克自治州', 654000);
