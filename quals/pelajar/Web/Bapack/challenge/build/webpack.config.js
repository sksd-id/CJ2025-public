import HtmlWebpackPlugin from 'html-webpack-plugin';
import CspHtmlWebpackPlugin from 'csp-html-webpack-plugin';

const SkypackRegexImport = "export \\* from '([^']+)'";

async function getScriptSrcFromSkypack(src) {
  const skypackUrl = `https://cdn.skypack.dev/${src}/`;
  const response = await fetch(skypackUrl);
  const text = await response.text();
  const scriptSrc = text.match(SkypackRegexImport);
  return [skypackUrl, "https://cdn.skypack.dev" + scriptSrc[1].split("dist=")[0]];
}

export default {
  output: {
    crossOriginLoading: "anonymous",
    libraryTarget: "module",
    filename: 'index.js',
  },
  experiments: {
    outputModule: true,
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './src/index.html',
      inject: "head",
      scriptLoading: "module",
    }),
    new CspHtmlWebpackPlugin({
      'script-src': ["'self'", ...(await getScriptSrcFromSkypack("showdown")), ...(await getScriptSrcFromSkypack("dompurify"))],
      'style-src': ["'self'"],
      'img-src': ["'self'"],
      'font-src': ["'self'"],
      'frame-src': ["'self'"],
      'connect-src': ["'self'"],
      'frame-ancestors': ["'self'"],
    }, {
      nonceEnabled: {
        'script-src': false,
        'style-src': false
      },
    })
  ],
}; 