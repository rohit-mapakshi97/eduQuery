import React, { useRef, useState } from 'react';
import { InteractiveNvlWrapper } from '@neo4j-nvl/react';
import VisualizationModal from './VisualizationModal';

const DataModelVisualization = () => {
  const [showModal, setShowModal] = useState(false);
  const nvlRef = useRef(null);

  const nodes = [
    { id: 'Instructor', caption: 'Instructor', color: '#E07A5F' },
    { id: 'Assessment', caption: 'Assessment', color: '#F4A261' },
    { id: 'Course', caption: 'Course', color: '#F2CC8F' },
    { id: 'Module', caption: 'Module', color: '#81B29A' },
    { id: 'Student', caption: 'Student', color: '#3D405B' },
  ];

  const relationships = [
    { id: '1', from: 'Student', to: 'Module', caption: 'COMPLETED_MODULE' },
    { id: '2', from: 'Module', to: 'Course', caption: 'PART_OF' },
    { id: '3', from: 'Assessment', to: 'Module', caption: 'PART_OF' },
    { id: '4', from: 'Student', to: 'Course', caption: 'ENROLLED_IN' },
    { id: '5', from: 'Instructor', to: 'Course', caption: 'TEACHES' },
    { id: '6', from: 'Student', to: 'Assessment', caption: 'COMPLETED_ASSESSMENT' },
  ];

  return (
    <>

      <div
        style={{
          position: 'relative',
          cursor: 'default',
          width: '100%',
          maxWidth: '1000px',
          aspectRatio: '16 / 9',
          background: '#1e1e1e',
          border: '1px solid #2AADA5',
          borderRadius: 12,
          margin: '0 auto 2rem auto',
          boxShadow: '0 0 12px rgba(0,0,0,0.3)',
          overflow: 'hidden',
          padding: '6px',
        }}
      >
        <InteractiveNvlWrapper
          ref={nvlRef}
          nodes={nodes}
          rels={relationships}
          layout={{ name: 'cose' }}
          nvlOptions={{
            initialZoom: 0.75,
            backgroundColor: '#1e1e1e',
            enableRelationshipCaptions: true,
            disableMouseInteractions: true,
          }}
          mouseEventCallbacks={{}}
        />

        {/* 🔍 Expand Icon */}
        <div
          onClick={() => setShowModal(true)}
          style={{
            position: 'absolute',
            bottom: 10,
            right: 12,
            background: '#333',
            color: '#fff',
            padding: '4px 8px',
            borderRadius: '6px',
            cursor: 'pointer',
            fontSize: '14px',
            opacity: 0.85,
          }}
        >
          ⤢ Expand
        </div>
      </div>

      <VisualizationModal
        show={showModal}
        handleClose={() => setShowModal(false)}
        nodes={nodes}
        relationships={relationships}
      />
    </>
  );
};

export default DataModelVisualization;
