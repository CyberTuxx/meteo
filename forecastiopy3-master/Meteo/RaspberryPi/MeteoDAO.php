<?php

require_once('DAO.php');

//retourne un Utilisateur ou nul
class MeteoDAO extends DAO
{
    public function getMeteo($order, $crois){
        require_once('Meteo.php');
        $res = $this->queryAll('SELECT * FROM Meteo WHERE date >= DATE_SUB(CURDATE(),INTERVAL 365 DAY) order by '.$order.' '.$crois);
        $meteo = array();
        if($res) {
            foreach ($res as $req) {
                $meteo[] = new Meteo($req['temp'], $req['pression'], $req['humidity'], $req['date']);
            }
        }
        else{
            return null;
        }
        return $meteo;
    }

    public function removeMeteo($date){
        $res = $this->queryAll("DELETE from Meteo where date = str_to_date('".$date."', '%Y-%m-%d %H:%i:%s')");
    }

    public function countMeteo(){
        $res = $this->queryAll('Select count(Date) as max from Meteo');
        if($res){
            foreach($res as $req) {
                return $req['max'];
            }
        }else{
            return 0;
        }
    }
}
