import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Slider from '@material-ui/core/Slider';
import Typography from '@material-ui/core/Typography';
import Tooltip from '@material-ui/core/Tooltip';

import './slider.css';

// const MySlider = withStyles({
//   root: {
//     color: '#8CBCB9',
//     height: 8,
//   },
//   thumb: {
//     height: 24,
//     width: 24,
//     backgroundColor: '#fff',
//     border: '2px solid currentColor',
//     marginTop: -8,
//     marginLeft: -12,
//     '&:focus,&:hover,&$active': {
//       boxShadow: 'inherit',
//     },

//   },
//   active: {},
//   valueLabel: {
//     left: 'calc(-50% + 4px)',
//   },
//   track: {
//     height: 8,
//     borderRadius: 4,
//   },
//   rail: {
//     height: 8,
//     borderRadius: 4,
//   },
// })(Slider);



// export default function TempSlider() {

//   return (
//     <div className="slider">
//         <div className="text">
//             Temperature
//         </div>
//         <MySlider valueLabelDisplay="auto" aria-label="slider" 
//                     defaultValue={0.5} max={1.0} min={0.1} step={0.1}
//                      />
      
//     </div>
//   );
// }

const TempSlider = withStyles({
      root: {
        color: '#8CBCB9',
        height: 8,
        width: 300,
        margin: 10
      },
      thumb: {
        height: 24,
        width: 24,
        backgroundColor: '#fff',
        border: '2px solid currentColor',
        marginTop: -8,
        marginLeft: -12,
        '&:focus,&:hover,&$active': {
          boxShadow: 'inherit',
        },
    
      },
      active: {},
      valueLabel: {
        left: 'calc(-50% + 4px)',
      },
      track: {
        height: 8,
        borderRadius: 4,
      },
      rail: {
        height: 8,
        borderRadius: 4,
      },
    })(Slider);

export default TempSlider;
    