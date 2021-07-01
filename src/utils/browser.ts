import Bowser from 'bowser';

const parser = Bowser.getParser(window.navigator.userAgent);
const browserName = parser.getBrowserName(true);

const getMediaFormat = () => {
  // returns (best) supported media format
  // either `dash` or `hls`
  if (browserName === 'safari') {
    return 'hls';
  }
  return 'dash';
};

// eslint-disable-next-line import/prefer-default-export
export { getMediaFormat };
