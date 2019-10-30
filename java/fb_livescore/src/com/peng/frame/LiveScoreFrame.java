package com.peng.frame;

import com.peng.bean.MatchBean;
import com.peng.bean.MatchCascadeBean;
import com.peng.bean.MatchNumBean;
import com.peng.repository.LiveDataRepository;
import com.peng.repository.MacthCascadeRepository;
import com.peng.repository.MatchNumRepository;
import com.peng.util.DateUtil;

import javax.swing.*;
import javax.swing.table.JTableHeader;
import java.awt.*;
import java.text.ParseException;
import java.util.Date;
import java.util.List;

public class LiveScoreFrame extends JFrame {


    private static final long serialVersionUID = 3218784607640603309L;

    public LiveScoreFrame() throws ParseException {
        super();
        setTitle("竞彩数据分析工具");

        setBounds(400, 200, 900, 600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);


        JPanel controlPanel = new JPanel();
        JLabel dateLabel = new JLabel("日期");
        JTextField txt1 = new JTextField(10);
        txt1.setText(DateUtil.getDateFormat().format(new Date()));

        // 定义日历控件面板类
        CalendarPanel calendarPanel = new CalendarPanel(txt1, "yyyy-MM-dd");
        getContentPane().add(calendarPanel);


        calendarPanel.initCalendarPanel();
        controlPanel.add(dateLabel);
        controlPanel.add(txt1);

        JButton btn = new JButton("读取数据");

        controlPanel.add(btn);

        // 将滚动面板添加到边界布局的中间
        getContentPane().add(controlPanel, BorderLayout.NORTH);

        JTabbedPane jTabbedPane = new JTabbedPane();
        Date selectDate = DateUtil.getDateFormat().parse(txt1.getText());
        jTabbedPane.add("赛事数据", this.getData1(selectDate));
        jTabbedPane.add("串关场次分析", this.getData2(selectDate));
        jTabbedPane.add("赛事分析", this.getData3(selectDate));

        jTabbedPane.setSelectedIndex(0);
        getContentPane().add(jTabbedPane, BorderLayout.CENTER);

        btn.addActionListener(e -> {
            try {
                jTabbedPane.setComponentAt(0,this.getData1(DateUtil.getDateFormat().parse(txt1.getText())));
                jTabbedPane.setComponentAt(1,this.getData2(DateUtil.getDateFormat().parse(txt1.getText())));
                jTabbedPane.setComponentAt(2,this.getData3(DateUtil.getDateFormat().parse(txt1.getText())));
            } catch (ParseException ex) {
                ex.printStackTrace();
            }
        });
    }

    private void setTableHeader(JTable table) {
        JTableHeader tableHeader = table.getTableHeader();
        tableHeader.setPreferredSize(new Dimension(tableHeader.getWidth(), 30));
        table.setRowHeight(25);
    }


    private JScrollPane getData1(Date date) {

        String[] columnNames = new String[]{"赛事编号", "比赛时间", "赛事", "状态", "主队", "客队", "赔率(胜)", "赔率(胜)", "赔率(胜)", "比分", "赛果"};// 定义表格列名数组
        List<MatchBean> matchBeanList = LiveDataRepository.getMatchData(date);

        String[][] rowData = new String[matchBeanList.size()][11];

        for (int i = 0; i < matchBeanList.size(); i++) {
            MatchBean matchBean = matchBeanList.get(i);
            String status = "已完成";
            if (matchBean.getStatus().equals("2")){
                status = "取消";
            }else  if (matchBean.getStatus().equals("0")){
                status = "未完成";
            }
            rowData[i] = new String[]{matchBean.getMatchNum(), matchBean.getLiveDate(), matchBean.getGroupName(), status, matchBean.getHostTeam(),
                    matchBean.getGuestTeam(), String.valueOf(matchBean.getOdds()[0]), String.valueOf(matchBean.getOdds()[1]), String.valueOf(matchBean.getOdds()[2]),
                    String.format("%s:%s", matchBean.getHostNum(), matchBean.getGuestNum()), matchBean.getResult()};
        }


        JTable table = new JTable(rowData, columnNames);
        table.setBorder(BorderFactory.createLineBorder(Color.GRAY));
        this.setTableHeader(table);
        return new JScrollPane(table);
    }

    private JScrollPane getData2(Date date) {


        String[] columnNames = new String[]{"串关场次", "胜平负组合", "当前遗漏值", "赔率"};// 定义表格列名数组
        List<MatchCascadeBean> matchCascadeBeans = MacthCascadeRepository.getMatchCascadeData(date);
        String[][] rowData = new String[matchCascadeBeans.size() * 9][4];

        for (int i = 0; i < matchCascadeBeans.size(); i++) {
            MatchCascadeBean matchCascadeBean = matchCascadeBeans.get(i);
            int j = i * 9;
            rowData[j] = new String[]{matchCascadeBean.getMatchCascadeNum(), "胜胜", String.valueOf(matchCascadeBean.getSs()), ""};
            rowData[j + 1] = new String[]{matchCascadeBean.getMatchCascadeNum(), "胜平", String.valueOf(matchCascadeBean.getSp()), ""};
            rowData[j + 2] = new String[]{matchCascadeBean.getMatchCascadeNum(), "胜负", String.valueOf(matchCascadeBean.getSf()), ""};
            rowData[j + 3] = new String[]{matchCascadeBean.getMatchCascadeNum(), "平胜", String.valueOf(matchCascadeBean.getPs()), ""};
            rowData[j + 4] = new String[]{matchCascadeBean.getMatchCascadeNum(), "平平", String.valueOf(matchCascadeBean.getPp()), ""};
            rowData[j + 5] = new String[]{matchCascadeBean.getMatchCascadeNum(), "平负", String.valueOf(matchCascadeBean.getPf()), ""};
            rowData[j + 6] = new String[]{matchCascadeBean.getMatchCascadeNum(), "负胜", String.valueOf(matchCascadeBean.getFs()), ""};
            rowData[j + 7] = new String[]{matchCascadeBean.getMatchCascadeNum(), "负平", String.valueOf(matchCascadeBean.getFp()), ""};
            rowData[j + 8] = new String[]{matchCascadeBean.getMatchCascadeNum(), "负负", String.valueOf(matchCascadeBean.getFf()), ""};
        }


        JTable table = new JTable(rowData, columnNames);
        table.setBorder(BorderFactory.createLineBorder(Color.GRAY));
        this.setTableHeader(table);
        return new JScrollPane(table);
    }

    private JScrollPane getData3(Date date) {
        String[] columnNames = new String[]{"赛事编号", "0球", "1球3球", "2球4球", "5球6球7球"
        };
        List<MatchNumBean> matchNumBeans = MatchNumRepository.getMatchNumData(date);
        String[][] rowData = new String[matchNumBeans.size()][5];
        for (int i = 0; i < matchNumBeans.size(); i++) {
            MatchNumBean matchNumBean = matchNumBeans.get(i);
            rowData[i] = new String[]{matchNumBean.getMatchNum(), String.valueOf(matchNumBean.getZero()),
                    String.valueOf(matchNumBean.getOne_three()), String.valueOf(matchNumBean.getTwo_four()),
                    String.valueOf(matchNumBean.getFive_())};
        }


        JTable table = new JTable(rowData, columnNames);
        table.setBorder(BorderFactory.createLineBorder(Color.GRAY));
        this.setTableHeader(table);
        return new JScrollPane(table);
    }
}

