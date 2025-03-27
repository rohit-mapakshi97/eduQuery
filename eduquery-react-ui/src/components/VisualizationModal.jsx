import React, { useRef, useEffect } from 'react';
import { Modal, Button } from 'react-bootstrap';
import { InteractiveNvlWrapper } from '@neo4j-nvl/react';

const VisualizationModal = ({ show, handleClose, nodes, relationships }) => {
  const wrapperRef = useRef(null);

  useEffect(() => {
    if (show) {
      const timeout = setTimeout(() => {
        if (wrapperRef.current?.zoomToFit) {
          wrapperRef.current.zoomToFit();
        }
      }, 300); // slight delay to wait for layout and size to apply

      return () => clearTimeout(timeout);
    }
  }, [show]);

  return (
    <Modal
      show={show}
      onHide={handleClose}
      size="xl"
      centered
      dialogClassName="custom-modal-size"
    >
      <Modal.Header closeButton>
        <Modal.Title>Data Model</Modal.Title>
      </Modal.Header>

      <Modal.Body style={{ padding: 0, backgroundColor: '#1e1e1e' }}>
        <div style={{ width: '100%', height: '80vh' }}>
          <InteractiveNvlWrapper
            ref={wrapperRef}
            nodes={nodes}
            rels={relationships}
            layout={{ name: 'cose' }}
            nvlOptions={{
              initialZoom: 1.5,
              backgroundColor: '#1e1e1e',
              enableRelationshipCaptions: true,
              draggable: true,
            }}
            mouseEventCallbacks={{
              onHover: (el, hits, evt) => console.log('Hover:', el),
              onPan: (evt) => console.log('Pan:', evt),
              onZoom: (z) => console.log('Zoom:', z),
              onNodeClick: (node) => console.log('Node clicked:', node),
              onNodeDoubleClick: (node) => console.log('Double click:', node),
              onNodeRightClick: (node) => console.log('Right click:', node),
              onRelationshipClick: (rel) => console.log('Relationship clicked:', rel),
              onRelationshipRightClick: (rel) => console.log('Relationship right-click:', rel),
              onRelationshipDoubleClick: (rel) => console.log('Relationship double-click:', rel),
              onCanvasClick: (evt) => console.log('Canvas clicked:', evt),
              onCanvasRightClick: (evt) => console.log('Canvas right-clicked', evt),
              onDrag: (nodes) => console.log('Nodes dragged:', nodes),
            }}
          />
        </div>
      </Modal.Body>

      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Close
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default VisualizationModal;
