/* global SETTINGS: false */
require('react-hot-loader/patch');
import React from 'react';
import ReactDOM from 'react-dom';

import USwitchPlayer from '../components/USwitchPlayer';
const videoSource = SETTINGS.videofile;

const videoDiv = document.querySelector('#odl-video-player');
if (videoDiv) {
  ReactDOM.render(
    <USwitchPlayer id='omniPlayer' src={videoSource.src}
      description={videoSource.description}
      title={videoSource.title}/>, videoDiv);
}



