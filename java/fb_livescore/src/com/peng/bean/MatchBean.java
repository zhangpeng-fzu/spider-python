package com.peng.bean;

public class MatchBean {

    private String matchNum;
    private String liveDate;
    private String groupName;
    private String status;
    private String hostTeam;
    private String guestTeam;
    private Float[] odds;
    private int hostNum;
    private int guestNum;
    private String result;
    private int num;


    public String getMatchNum() {
        return this.matchNum;
    }

    public void setMatchNum(String matchNum) {
        this.matchNum = matchNum;
    }

    public String getLiveDate() {
        return this.liveDate;
    }

    public void setLiveDate(String liveDate) {
        this.liveDate = liveDate;
    }

    public String getGroupName() {
        return this.groupName;
    }

    public void setGroupName(String groupName) {
        this.groupName = groupName;
    }

    public String getStatus() {
        return this.status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getHostTeam() {
        return this.hostTeam;
    }

    public void setHostTeam(String hostTeam) {
        this.hostTeam = hostTeam;
    }

    public String getGuestTeam() {
        return this.guestTeam;
    }

    public void setGuestTeam(String guestTeam) {
        this.guestTeam = guestTeam;
    }

    public Float[] getOdds() {
        return this.odds;
    }

    public void setOdds(Float[] odds) {
        this.odds = odds;
    }

    public int getHostNum() {
        return this.hostNum;
    }

    public void setHostNum(int hostNum) {
        this.hostNum = hostNum;
    }

    public int getGuestNum() {
        return this.guestNum;
    }

    public void setGuestNum(int guestNum) {
        this.guestNum = guestNum;
    }

    public String getResult() {
        if (this.hostNum > this.guestNum) {
            this.result = "胜";
        } else if (this.hostNum == this.guestNum) {
            this.result = "平";
        } else {
            this.result = "负";
        }
        return this.result;
    }

    public void setResult(String result) {
        this.result = result;
    }

    public int getNum() {
        return this.hostNum + this.guestNum;
    }

    public void setNum(int num) {
        this.num = num;
    }
}
