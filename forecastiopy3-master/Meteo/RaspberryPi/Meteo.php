<?php

class Meteo
{
    private $_temp;

    private $_pression;

    private $_humidity;

    private $_date;



    public function __construct($temp = 0, $pression = "", $humidity = "", $date = 0)
    {
        $this->_temp = $temp;
        $this->_date = $date;
        $this->_humidity = $humidity;
        $this->_pression = $pression;
    }

    public function getTemp() {
        return $this->_temp;
    }

    public function getDate() {
        return $this->_date;
    }

    public function getHumidity() {
        return $this->_humidity;
    }

    public function getpression(){
        return $this->_pression;
    }

}?>
